#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A100 v16 Fixed Ranker

Added over v12:
- Accumulation Index
- Distribution Index
- Bubble Index
- Confidence Score
- Auto entry/stop/targets
- 24h/3d/7d breakout probability estimate
- Risk level
- AI comment block
"""

import os, time, requests, asyncio, threading, traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
CG_KEY = os.getenv("COINGLASS_API_KEY", "").strip()
DEFAULT_SYMBOLS = [x.strip().upper() for x in os.getenv(
    "DEFAULT_SYMBOLS",
    "BTC,ETH,SOL,ARKM,SYN,SENT,ALT,VANRY,CELO,COTI,NFP,TIA,INJ,WLD,ZEC,KAITO,APE"
).split(",") if x.strip()]
SCORE_ALERT = float(os.getenv("SCORE_ALERT", "85"))
TOP_SCAN_LIMIT = int(os.getenv("TOP_SCAN_LIMIT", "50"))

BINANCE_MARKET = "https://data-api.binance.vision"
UPBIT = "https://api.upbit.com"
BITHUMB = "https://api.bithumb.com"
CG_BASE = "https://open-api-v4.coinglass.com"

def log(msg: str):
    print(msg, flush=True)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"A100 v16 Fixed Ranker is running"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    log(f"Health server listening on port {port}")
    server.serve_forever()

def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x) if x is not None else default
    except Exception:
        return default

def pct(new: float, old: float) -> float:
    return 0.0 if old == 0 else (new - old) / abs(old) * 100.0

def avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def sma(values: List[float], n: int) -> Optional[float]:
    return sum(values[-n:]) / n if len(values) >= n else None

def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def get_json(url: str, params=None, headers=None):
    r = requests.get(url, params=params or {}, headers=headers or {}, timeout=18)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} {url} {r.text[:220]}")
    return r.json()

def grade(score: float) -> str:
    if score >= 92: return "S"
    if score >= 85: return "A+"
    if score >= 78: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "PASS"

def rsi(closes: List[float], period: int = 14) -> float:
    if len(closes) <= period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(-period, 0):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    ag, al = avg(gains), avg(losses)
    if al == 0:
        return 100.0
    rs = ag / al
    return 100 - (100 / (1 + rs))

def ema(values: List[float], n: int) -> List[float]:
    if not values:
        return []
    k = 2 / (n + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append(v * k + out[-1] * (1 - k))
    return out

def macd_hist(closes: List[float]) -> float:
    if len(closes) < 35:
        return 0.0
    e12 = ema(closes, 12)
    e26 = ema(closes, 26)
    macd = [a - b for a, b in zip(e12[-len(e26):], e26)]
    sig = ema(macd, 9)
    return macd[-1] - sig[-1]

def atr(highs: List[float], lows: List[float], closes: List[float], n: int = 14) -> float:
    if len(closes) < n + 1:
        return 0.0
    trs = []
    for i in range(-n, 0):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        trs.append(tr)
    return avg(trs)

# Binance market data
def get_binance_klines(pair: str, interval: str = "4h", limit: int = 120) -> List[Dict[str, float]]:
    rows = get_json(f"{BINANCE_MARKET}/api/v3/klines", {"symbol": pair, "interval": interval, "limit": limit})
    return [{
        "open": safe_float(r[1]),
        "high": safe_float(r[2]),
        "low": safe_float(r[3]),
        "close": safe_float(r[4]),
        "quote_volume": safe_float(r[7]),
        "trades": safe_float(r[8]),
        "taker_buy_quote": safe_float(r[10]),
    } for r in rows]

def get_binance_top_usdt(limit: int = 50) -> List[str]:
    data = get_json(f"{BINANCE_MARKET}/api/v3/ticker/24hr")
    rows = []
    for x in data:
        sym = x.get("symbol", "")
        if not sym.endswith("USDT"):
            continue
        if any(bad in sym for bad in ["UPUSDT", "DOWNUSDT", "BULLUSDT", "BEARUSDT"]):
            continue
        qv = safe_float(x.get("quoteVolume"))
        rows.append((sym.replace("USDT", ""), qv))
    rows.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in rows[:limit]]

# CoinGlass
def cg_get(path: str, params: Dict[str, Any]) -> Optional[Any]:
    if not CG_KEY:
        log("CoinGlass key empty")
        return None
    try:
        data = get_json(CG_BASE + path, params, {"CG-API-KEY": CG_KEY, "accept": "application/json"})
        if "data" not in data:
            log(f"CoinGlass no data field: {path} {str(data)[:200]}")
            return None
        return data["data"]
    except Exception as e:
        log(f"CoinGlass error {path} {params}: {e}")
        return None

def cg_rows(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ["list", "data", "rows", "items"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        return [data]
    return []

def cg_num(row: Dict[str, Any], keys: List[str], default=0.0) -> float:
    for k in keys:
        if k in row:
            return safe_float(row.get(k), default)
    return default

def cg_oi(symbol: str) -> Tuple[float, float, str]:
    data = cg_get("/api/futures/open-interest/aggregated-history", {
        "symbol": symbol, "interval": "4h", "limit": 30, "unit": "usd"
    })
    rows = cg_rows(data)
    if len(rows) >= 6:
        now = cg_num(rows[-1], ["close", "value", "openInterest", "sumOpenInterest"], 0)
        prev = cg_num(rows[-6], ["close", "value", "openInterest", "sumOpenInterest"], 0)
        chg = pct(now, prev)
        score = min(max(chg * 1.0, 0), 15)
        return score, round(chg, 2), "OI OK"
    return 0.0, 0.0, "OI 없음"

def cg_funding(symbol: str) -> Tuple[float, float, str]:
    data = cg_get("/api/futures/funding-rate/oi-weight-history", {
        "symbol": symbol, "interval": "4h", "limit": 10
    })
    rows = cg_rows(data)
    rate = 0.0
    trend_bonus = 0
    if rows:
        vals = []
        for row in rows[-5:]:
            val = cg_num(row, ["close", "rate", "fundingRate", "value"], 0)
            if abs(val) < 1: val *= 100
            vals.append(val)
        rate = vals[-1] if vals else 0
        if len(vals) >= 3 and vals[-1] > vals[0] and vals[-1] <= 0.03:
            trend_bonus = 2
    if -0.08 <= rate < -0.01: score = 8 + trend_bonus
    elif -0.01 <= rate <= 0.02: score = 7 + trend_bonus
    elif 0.02 < rate <= 0.05: score = 3
    else: score = 1
    return min(score, 10), round(rate, 5), "Funding OK" if rows else "Funding 없음"

def cg_taker(symbol: str) -> Tuple[float, float, str]:
    data = cg_get("/api/futures/aggregated-taker-buy-sell-volume/history", {
        "symbol": symbol, "interval": "4h", "limit": 10
    })
    rows = cg_rows(data)
    if rows:
        row = rows[-1]
        buy = cg_num(row, ["buy", "buyVolume", "takerBuyVol", "takerBuyVolume"], 0)
        sell = cg_num(row, ["sell", "sellVolume", "takerSellVol", "takerSellVolume"], 0)
        ratio = buy / sell if sell else 1.0
        if 0.85 <= ratio <= 1.35: score = 5
        elif 1.35 < ratio <= 2.0: score = 4
        elif 0.65 <= ratio < 0.85: score = 3
        else: score = 1
        return score, round(ratio, 3), "Taker OK"
    return 0.0, 0.0, "Taker 없음"

def cg_long_short(symbol: str) -> Tuple[float, float, str]:
    endpoints = [
        ("/api/futures/global-long-short-account-ratio/history", {"symbol": symbol, "interval": "4h", "limit": 10}),
        ("/api/futures/top-long-short-account-ratio/history", {"symbol": symbol, "interval": "4h", "limit": 10}),
    ]
    for path, params in endpoints:
        data = cg_get(path, params)
        rows = cg_rows(data)
        if rows:
            row = rows[-1]
            ratio = cg_num(row, ["longShortRatio", "ratio", "longShortRate"], 0)
            long_pct = cg_num(row, ["longAccount", "longRate", "long"], 0)
            if ratio and 0.6 <= ratio <= 1.15: score = 3
            elif ratio and 1.15 < ratio <= 1.6: score = 2
            else: score = 1
            return score, round(ratio or long_pct, 3), "L/S OK"
    return 0.0, 0.0, "L/S 없음"

def cg_liquidation(symbol: str) -> Tuple[float, str, str]:
    endpoints = [
        ("/api/futures/liquidation/history", {"symbol": symbol, "interval": "4h", "limit": 12}),
        ("/api/futures/liquidation/aggregated-history", {"symbol": symbol, "interval": "4h", "limit": 12}),
    ]
    for path, params in endpoints:
        data = cg_get(path, params)
        rows = cg_rows(data)
        if rows:
            long_liq = 0.0
            short_liq = 0.0
            for row in rows[-6:]:
                long_liq += cg_num(row, ["longLiquidation", "longLiquidationUsd", "longVolUsd", "long"], 0)
                short_liq += cg_num(row, ["shortLiquidation", "shortLiquidationUsd", "shortVolUsd", "short"], 0)
            if short_liq > long_liq * 1.5 and short_liq > 0:
                score, bias = 5, "상방 숏청산 우세"
            elif long_liq > short_liq * 1.5 and long_liq > 0:
                score, bias = 1, "하방 롱청산 위험"
            else:
                score, bias = (3 if (long_liq + short_liq) > 0 else 0), "청산 중립/부족"
            return score, bias, f"{bias} L:{long_liq:.0f} S:{short_liq:.0f}"
    return 0.0, "청산데이터 없음", "청산데이터 없음"

def cg_snapshot(symbol: str) -> Dict[str, Any]:
    oi_s, oi_chg, oi_note = cg_oi(symbol)
    fund_s, fund_rate, fund_note = cg_funding(symbol)
    taker_s, taker_ratio, taker_note = cg_taker(symbol)
    ls_s, ls_ratio, ls_note = cg_long_short(symbol)
    liq_s, liq_bias, liq_note = cg_liquidation(symbol)
    total = oi_s + fund_s + taker_s + ls_s + liq_s
    return {
        "oi_score": oi_s, "oi_change": oi_chg, "oi_note": oi_note,
        "funding_score": fund_s, "funding_rate": fund_rate, "funding_note": fund_note,
        "taker_score": taker_s, "taker_ratio": taker_ratio, "taker_note": taker_note,
        "ls_score": ls_s, "ls_ratio": ls_ratio, "ls_note": ls_note,
        "liq_score": liq_s, "liq_bias": liq_bias, "liq_note": liq_note,
        "total": total,
    }

def cg_test_text(symbol="BTC") -> str:
    sym = symbol.upper().replace("USDT", "")
    snap = cg_snapshot(sym)
    return (
        f"🧪 <b>CoinGlass v16 테스트 {sym}</b>\n"
        f"OI: {snap['oi_change']}% / {snap['oi_score']} ({snap['oi_note']})\n"
        f"Funding: {snap['funding_rate']}% / {snap['funding_score']} ({snap['funding_note']})\n"
        f"Taker: {snap['taker_ratio']} / {snap['taker_score']} ({snap['taker_note']})\n"
        f"L/S: {snap['ls_ratio']} / {snap['ls_score']} ({snap['ls_note']})\n"
        f"Liquidation: {snap['liq_score']} ({snap['liq_note']})\n"
        f"CG total: {snap['total']}/38"
    )

# KR markets
def upbit_markets() -> List[str]:
    data = get_json(f"{UPBIT}/v1/market/all", {"isDetails": "false"})
    return [x["market"] for x in data if x.get("market", "").startswith("KRW-")]

def upbit_tickers(markets: List[str]) -> Dict[str, Dict[str, float]]:
    out = {}
    for i in range(0, len(markets), 100):
        chunk = markets[i:i+100]
        data = get_json(f"{UPBIT}/v1/ticker", {"markets": ",".join(chunk)})
        for x in data:
            sym = x["market"].replace("KRW-", "")
            out[sym] = {
                "price": safe_float(x.get("trade_price")),
                "change_pct": safe_float(x.get("signed_change_rate")) * 100,
                "acc_trade_price_24h": safe_float(x.get("acc_trade_price_24h")),
            }
        time.sleep(0.08)
    return out

def bithumb_tickers() -> Dict[str, Dict[str, float]]:
    data = get_json(f"{BITHUMB}/public/ticker/ALL_KRW")
    raw = data.get("data", {})
    out = {}
    for sym, x in raw.items():
        if sym == "date" or not isinstance(x, dict):
            continue
        out[sym.upper()] = {
            "price": safe_float(x.get("closing_price")),
            "change_pct": safe_float(x.get("fluctate_rate_24H")),
            "acc_trade_price_24h": safe_float(x.get("acc_trade_value_24H")),
        }
    return out

def kr_market_snapshot() -> Dict[str, Dict[str, float]]:
    result = {}
    try:
        ut = upbit_tickers(upbit_markets())
        for sym, x in ut.items():
            result.setdefault(sym, {})
            result[sym]["upbit_value"] = x["acc_trade_price_24h"]
            result[sym]["upbit_change"] = x["change_pct"]
    except Exception as e:
        log(f"Upbit error: {e}")
    try:
        bt = bithumb_tickers()
        for sym, x in bt.items():
            result.setdefault(sym, {})
            result[sym]["bithumb_value"] = x["acc_trade_price_24h"]
            result[sym]["bithumb_change"] = x["change_pct"]
    except Exception as e:
        log(f"Bithumb error: {e}")
    for sym, x in result.items():
        x["kr_value"] = safe_float(x.get("upbit_value")) + safe_float(x.get("bithumb_value"))
        vals = []
        if "upbit_change" in x: vals.append(x["upbit_change"])
        if "bithumb_change" in x: vals.append(x["bithumb_change"])
        x["kr_change"] = avg(vals) if vals else 0.0
    return result

def kr_score_for_symbol(sym: str, kr: Dict[str, Dict[str, float]]) -> Tuple[float, str, float, float]:
    x = kr.get(sym.upper())
    if not x:
        return 0.0, "KR 미상장/데이터 없음", 0.0, 0.0
    value = x.get("kr_value", 0)
    chg = x.get("kr_change", 0)
    score = 0
    if value >= 10_000_000_000: score += 4
    if value >= 30_000_000_000: score += 4
    if value >= 100_000_000_000: score += 4
    if chg > 2: score += 3
    if chg > 5: score += 3
    score = min(score, 15)
    return score, f"KR거래대금 {value/100000000:.1f}억 / KR등락 {chg:.2f}%", value, chg

@dataclass
class Result:
    pair: str
    price: float
    score: float
    grade: str
    chart_score: float
    volume_score: float
    kr_score: float
    cg_score: float
    momentum_score: float
    risk_score: float
    vol_ratio: float
    buy_ratio: float
    rsi14: float
    support: float
    resistance: float
    cg_text: str
    liq_text: str
    kr_note: str
    note: str
    accumulation: float
    distribution: float
    bubble: float
    confidence: float
    prob24: float
    prob3d: float
    prob7d: float
    risk_level: str
    entry_low: float
    entry_high: float
    stop: float
    target1: float
    target2: float
    ai_comment: str

def risk_label(x: float) -> str:
    if x >= 70: return "HIGH"
    if x >= 40: return "MEDIUM"
    return "LOW"

def compute_ai_indices(price, ma20, ma60, vol_ratio, buy_ratio, rsi14, macd, chg_24, atr_v, cg, kr_score, kr_value, kr_chg):
    oi = cg["oi_change"]
    funding = cg["funding_rate"]
    # Accumulation: quiet/constructive chart + OI/KR/volume without too much bubble
    accumulation = 0
    accumulation += clamp(oi * 2, 0, 25)
    accumulation += 18 if -0.08 <= funding <= 0.02 else (8 if funding <= 0.05 else 2)
    accumulation += clamp((vol_ratio - 1) * 18, 0, 18)
    accumulation += 12 if buy_ratio >= 0.52 else 4
    accumulation += kr_score * 1.2
    accumulation += 10 if price >= ma20 else 3
    accumulation += 8 if macd > 0 else 0
    accumulation = clamp(accumulation)

    # Distribution: high price extension + high vol but weakening buy pressure
    distribution = 0
    distribution += clamp(chg_24 * 1.2, 0, 35)
    distribution += clamp((vol_ratio - 2) * 12, 0, 25)
    distribution += 20 if buy_ratio < 0.48 else (10 if buy_ratio < 0.52 else 0)
    distribution += 15 if rsi14 > 75 else (8 if rsi14 > 68 else 0)
    distribution += 10 if funding > 0.05 else 0
    distribution = clamp(distribution)

    # Bubble: too hot / crowded / extended
    bubble = 0
    bubble += clamp(chg_24 * 1.5, 0, 35)
    bubble += 20 if rsi14 > 75 else (10 if rsi14 > 68 else 0)
    bubble += 15 if funding > 0.05 else (6 if funding > 0.02 else 0)
    bubble += clamp((vol_ratio - 3) * 10, 0, 20)
    bubble += 10 if price > ma60 * 1.25 else 0
    bubble = clamp(bubble)

    # Confidence: data coverage + alignment
    coverage = 0
    if cg["oi_note"] != "OI 없음": coverage += 18
    if cg["funding_note"] != "Funding 없음": coverage += 14
    if cg["taker_note"] != "Taker 없음": coverage += 10
    if cg["liq_note"] != "청산데이터 없음": coverage += 8
    if kr_value > 0: coverage += 10
    alignment = 0
    if price >= ma20: alignment += 10
    if vol_ratio >= 1.2: alignment += 8
    if buy_ratio >= 0.52: alignment += 8
    if macd > 0: alignment += 7
    if accumulation > distribution: alignment += 7
    confidence = clamp(coverage + alignment)

    # Probability heuristic, not guarantee
    base = 35 + (accumulation * 0.35) + (confidence * 0.20) - (bubble * 0.20) - (distribution * 0.15)
    prob24 = clamp(base, 5, 95)
    prob3d = clamp(base + 8 if accumulation > 60 else base, 5, 97)
    prob7d = clamp(base + 14 if accumulation > 70 else base + 5, 5, 98)

    # Strategy levels
    atr_pct = atr_v / price if price else 0.03
    band = max(atr_pct, 0.025)
    entry_low = price * (1 - band * 0.55)
    entry_high = price * (1 + band * 0.15)
    stop = price * (1 - band * 1.2)
    target1 = price * (1 + band * 1.8)
    target2 = price * (1 + band * 3.2)

    risk_value = (bubble * 0.55 + distribution * 0.45)
    return {
        "accumulation": round(accumulation, 1),
        "distribution": round(distribution, 1),
        "bubble": round(bubble, 1),
        "confidence": round(confidence, 1),
        "prob24": round(prob24, 1),
        "prob3d": round(prob3d, 1),
        "prob7d": round(prob7d, 1),
        "risk_level": risk_label(risk_value),
        "entry_low": round(entry_low, 8),
        "entry_high": round(entry_high, 8),
        "stop": round(stop, 8),
        "target1": round(target1, 8),
        "target2": round(target2, 8),
    }

def ai_comment(score, acc, dist, bubble, confidence, cg, kr_score, vol_ratio, buy_ratio, price, ma20):
    parts = []
    if score >= 85: parts.append("A+ 후보권")
    elif score >= 70: parts.append("관찰 후보")
    else: parts.append("아직 대기")
    if acc >= 75: parts.append("매집지수 강함")
    elif acc >= 55: parts.append("매집 가능성 관찰")
    if dist >= 70: parts.append("분배 위험 높음")
    if bubble >= 70: parts.append("과열 주의")
    if cg["oi_score"] >= 7: parts.append("OI 증가")
    if cg["funding_score"] >= 7: parts.append("펀딩 양호")
    if cg["liq_score"] >= 4: parts.append("청산 방향성 감지")
    if kr_score >= 8: parts.append("국내 현물 수급")
    if vol_ratio >= 1.5: parts.append("거래량 증가")
    if buy_ratio >= 0.56: parts.append("매수압 우세")
    if price < ma20: parts.append("MA20 아래라 추격 금지")
    if confidence < 45: parts.append("데이터 신뢰도 낮음")
    return " / ".join(parts)

def analyze(symbol: str, kr: Optional[Dict[str, Dict[str, float]]] = None, interval: str = "4h") -> Result:
    symbol = symbol.upper().replace("USDT", "")
    pair = f"{symbol}USDT"
    log(f"analyze start: {pair}")
    kl = get_binance_klines(pair, interval, 120)
    if len(kl) < 60:
        raise RuntimeError(f"{pair} kline data too short: {len(kl)}")
    closes = [x["close"] for x in kl]
    highs = [x["high"] for x in kl]
    lows = [x["low"] for x in kl]
    qvols = [x["quote_volume"] for x in kl]
    buyq = [x["taker_buy_quote"] for x in kl]
    price = closes[-1]
    ma5 = sma(closes, 5) or price
    ma20 = sma(closes, 20) or price
    ma60 = sma(closes, 60) or price
    recent_low = min(lows[-30:])
    prev_low = min(lows[-60:-30])
    support = min(lows[-20:])
    resistance = max(highs[-20:])
    atr_v = atr(highs, lows, closes, 14)

    chart = 0
    if price > ma5: chart += 5
    if price > ma20: chart += 6
    if ma5 > ma20: chart += 4
    if price > ma60: chart += 3
    if recent_low >= prev_low * 0.98: chart += 2
    chart = min(chart, 20)

    vol_now = avg(qvols[-3:])
    vol_base = avg(qvols[-60:-15])
    vol_ratio = vol_now / vol_base if vol_base else 1.0
    buy_now = avg(buyq[-3:])
    buy_ratio = buy_now / vol_now if vol_now else 0.5

    volume = min(max((vol_ratio - 1) * 7, 0), 12)
    if buy_ratio > 0.60: volume += 3
    elif buy_ratio > 0.56: volume += 2
    elif buy_ratio > 0.52: volume += 1
    volume = min(volume, 15)

    rsi14 = rsi(closes, 14)
    mh = macd_hist(closes)
    momentum = 0
    if 45 <= rsi14 <= 68: momentum += 2
    if mh > 0: momentum += 2
    if closes[-1] > closes[-4]: momentum += 1

    kr = kr or {}
    kr_score, kr_note, kr_value, kr_chg = kr_score_for_symbol(symbol, kr)

    cg = cg_snapshot(symbol)
    cg_score = min(cg["total"] * 35 / 38, 35)
    cg_text = f"OI {cg['oi_change']}% / Funding {cg['funding_rate']}% / Taker {cg['taker_ratio']} / L/S {cg['ls_ratio']}"
    liq_text = cg["liq_note"]

    chg_24 = pct(closes[-1], closes[-7])
    risk = 10
    if chg_24 > 25: risk -= 3
    if chg_24 > 45: risk -= 4
    if price < ma20: risk -= 3
    risk = max(risk, 0)

    score = chart + volume + kr_score + cg_score + momentum + risk

    ai = compute_ai_indices(price, ma20, ma60, vol_ratio, buy_ratio, rsi14, mh, chg_24, atr_v, cg, kr_score, kr_value, kr_chg)

    notes = []
    if cg["oi_score"] >= 7: notes.append("OI 증가")
    if cg["funding_score"] >= 7: notes.append("펀딩 양호")
    if cg["liq_score"] >= 4: notes.append("청산 방향성")
    if vol_ratio < 1.5: notes.append("글로벌 거래량 부족")
    if buy_ratio < 0.52: notes.append("글로벌 매수압 약함")
    if price < ma20: notes.append("MA20 아래")
    if mh <= 0: notes.append("MACD 약함")
    if kr_score >= 8: notes.append("국내 현물 수급")
    if chg_24 > 35: notes.append("단기 급등 리스크")
    if not notes: notes.append("A100 조건 양호")

    comment = ai_comment(score, ai["accumulation"], ai["distribution"], ai["bubble"], ai["confidence"], cg, kr_score, vol_ratio, buy_ratio, price, ma20)

    result = Result(
        pair, round(price, 8), round(score, 2), grade(score),
        round(chart, 2), round(volume, 2), round(kr_score, 2),
        round(cg_score, 2), round(momentum, 2), round(risk, 2),
        round(vol_ratio, 2), round(buy_ratio, 3), round(rsi14, 2),
        round(support, 8), round(resistance, 8),
        cg_text, liq_text, kr_note, " / ".join(notes),
        ai["accumulation"], ai["distribution"], ai["bubble"], ai["confidence"],
        ai["prob24"], ai["prob3d"], ai["prob7d"], ai["risk_level"],
        ai["entry_low"], ai["entry_high"], ai["stop"], ai["target1"], ai["target2"],
        comment
    )
    log(f"analyze done: {pair} score={result.score}")
    return result

def scan(symbols: List[str], use_kr: bool = True) -> List[Result]:
    log(f"scan symbols={symbols}, use_kr={use_kr}")
    kr = kr_market_snapshot() if use_kr else {}
    out = []
    for s in symbols:
        try:
            out.append(analyze(s, kr))
        except Exception as e:
            log(f"{s} error: {e}")
            log(traceback.format_exc())
        time.sleep(0.12)
    return sorted(out, key=lambda x: x.score, reverse=True)


def bar(value: float, width: int = 10) -> str:
    try:
        v = max(0, min(100, float(value)))
    except Exception:
        v = 0
    filled = int(round(v / 100 * width))
    return "■" * filled + "□" * (width - filled)

def star(value: float) -> str:
    try:
        v = float(value)
    except Exception:
        v = 0
    if v >= 85:
        return "★★★★★"
    if v >= 70:
        return "★★★★☆"
    if v >= 55:
        return "★★★☆☆"
    if v >= 40:
        return "★★☆☆☆"
    return "★☆☆☆☆"

def final_action(score, acc, dist, bubble, conf, price, entry_low, entry_high):
    if conf < 35:
        return "데이터 부족 — 관망"
    if bubble >= 75 or dist >= 75:
        return "추격금지"
    if score >= 85 and acc >= 70:
        return "분할매수/적극검토"
    if score >= 70 and acc >= 55:
        return "눌림 분할매수"
    return "관망"

def one_line_reason(r):
    reasons = []
    if r.accumulation >= 70:
        reasons.append("매집 강함")
    if r.confidence >= 70:
        reasons.append("신뢰도 양호")
    if r.kr_score >= 8:
        reasons.append("KR수급")
    if r.cg_score >= 18:
        reasons.append("선물수급")
    if r.bubble >= 70:
        reasons.append("과열")
    if r.distribution >= 70:
        reasons.append("분배위험")
    if r.score < 60:
        reasons.append("점수 낮음")
    return " / ".join(reasons) if reasons else "뚜렷한 강점 부족"


def format_result(r: Result) -> str:
    smart = round((r.accumulation * 0.45 + r.confidence * 0.25 - r.bubble * 0.15 - r.distribution * 0.15), 1)
    squeeze = round(min(100, max(0, r.cg_score * 2 + (15 if r.accumulation >= 70 else 0))), 1)
    whale = round(min(100, max(0, (r.vol_ratio - 1) * 25 + (15 if r.buy_ratio > 0.56 else 0) + (10 if r.kr_score >= 8 else 0))), 1)
    action = final_action(r.score, r.accumulation, r.distribution, r.bubble, r.confidence, r.price, r.entry_low, r.entry_high)
    stage = "5단계 급등시작" if r.score >= 92 and r.vol_ratio >= 2 else ("4단계 폭발직전" if r.accumulation >= 80 else ("3단계 수급증가" if r.accumulation >= 65 else ("2단계 매집관찰" if r.accumulation >= 50 else "1단계 관찰")))
    warnings = []
    if r.bubble >= 70:
        warnings.append("과열")
    if r.distribution >= 70:
        warnings.append("분배")
    if r.confidence < 45:
        warnings.append("신뢰도 낮음")
    if "MA20 아래" in r.note:
        warnings.append("MA20 아래")
    warn_txt = " / ".join(warnings) if warnings else "특이위험 낮음"
    return (
        f"🟢 <b>{r.pair}</b> {star(r.score)}\n"
        f"<b>A100 SCORE</b> {r.score}점 / {r.grade}\n"
        f"AI결론: <b>{action}</b>\n"
        f"현재단계: <b>{stage}</b>\n"
        f"핵심이유: {one_line_reason(r)}\n\n"
        f"세력매집  {bar(r.accumulation)} {r.accumulation}%\n"
        f"스마트머니 {bar(smart)} {smart}%\n"
        f"고래대체  {bar(whale)} {whale}%\n"
        f"숏스퀴즈  {bar(squeeze)} {squeeze}%\n"
        f"신뢰도    {bar(r.confidence)} {r.confidence}%\n"
        f"분배위험  {bar(r.distribution)} {r.distribution}%\n"
        f"버블위험  {bar(r.bubble)} {r.bubble}%\n\n"
        f"가격: <code>{r.price}</code>\n"
        f"지지/저항: <code>{r.support}</code> / <code>{r.resistance}</code>\n"
        f"진입: <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절: <code>{r.stop}</code>\n"
        f"목표: <code>{r.target1}</code> / <code>{r.target2}</code>\n"
        f"확률: 24h {r.prob24}% | 3d {r.prob3d}% | 7d {r.prob7d}%\n\n"
        f"수급: KR {r.kr_score}/15 | CG {r.cg_score}/35 | Vol {r.vol_ratio}x | 매수비율 {r.buy_ratio}\n"
        f"CG: {r.cg_text}\n"
        f"KR: {r.kr_note}\n"
        f"경고: {warn_txt}\n"
        f"AI코멘트: {r.ai_comment}\n"
    )

def build_report(symbols: List[str], top_n: int = 10, use_kr: bool = True) -> str:
    results = scan(symbols, use_kr=use_kr)
    if not results:
        return "A100 결과 없음\n\nRender 로그 error 확인 필요"
    return "🔥 <b>A100 v16 Fixed Ranker TOP</b>\n\n" + "\n━━━━━━━━━━━━\n".join(format_result(r) for r in results[:top_n])

def build_kr_report(top_n: int = 20) -> str:
    kr = kr_market_snapshot()
    rows = []
    for sym, x in kr.items():
        rows.append((sym, x.get("kr_value", 0), x.get("kr_change", 0)))
    rows.sort(key=lambda x: x[1], reverse=True)
    lines = ["🇰🇷 <b>업비트+빗썸 KRW 거래대금 상위</b>\n"]
    for i, (sym, value, chg) in enumerate(rows[:top_n], 1):
        lines.append(f"{i}. <b>{sym}</b> | {value/100000000:.1f}억 | {chg:.2f}%")
    return "\n".join(lines)


def format_compact_rank(results: List[Result], top_n: int = 10) -> str:
    lines = ["⚡ <b>A100 v16 빠른 신호 랭킹</b>", ""]
    for i, r in enumerate(results[:top_n], 1):
        smart = round((r.accumulation * 0.45 + r.confidence * 0.25 - r.bubble * 0.15 - r.distribution * 0.15), 1)
        squeeze = round(min(100, max(0, r.cg_score * 2 + (15 if r.accumulation >= 70 else 0))), 1)
        action = final_action(r.score, r.accumulation, r.distribution, r.bubble, r.confidence, r.price, r.entry_low, r.entry_high)
        lines.append(
            f"{i}. <b>{r.pair}</b> {star(r.score)}\n"
            f"점수 {r.score} | 매집 {r.accumulation}% | 스마트 {smart}% | 스퀴즈 {squeeze}% | 신뢰 {r.confidence}%\n"
            f"판정: <b>{action}</b>\n"
            f"진입 <code>{r.entry_low}~{r.entry_high}</code> / 손절 <code>{r.stop}</code> / 목표 <code>{r.target1}</code>\n"
            f"이유: {one_line_reason(r)}"
        )
    return "\n\n".join(lines)

def build_compact_report(symbols: List[str], top_n: int = 10, use_kr: bool = True) -> str:
    results = scan(symbols, use_kr=use_kr)
    if not results:
        return "A100 결과 없음\n\nRender 로그 error 확인 필요"
    return format_compact_rank(results, top_n)

# Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 v16 시작\n/check\n/scan ARKM,SYN,SENT\n/top\n/best\n/rank\n/hot\n/risk ARKM,SYN\n/kr\n/cgtest BTC\n/myid")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"TELEGRAM_CHAT_ID = {update.effective_chat.id}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 v16 기본 리스트 분석 중...")
    await update.message.reply_text(build_report(DEFAULT_SYMBOLS, 10, True), parse_mode="HTML")

async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(context.args).strip()
    if not raw:
        await update.message.reply_text("예: /scan ARKM,SYN,SENT")
        return
    symbols = [x.strip().upper() for x in raw.replace(" ", "").split(",") if x.strip()]
    await update.message.reply_text("A100 v16 분석 중...")
    await update.message.reply_text(build_report(symbols, 10, True), parse_mode="HTML")

async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"A100 v16 거래량 상위 USDT {TOP_SCAN_LIMIT}개 스캔 중...")
    symbols = get_binance_top_usdt(TOP_SCAN_LIMIT)
    await update.message.reply_text(build_report(symbols, 10, True), parse_mode="HTML")


async def rank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 v16 빠른 랭킹 스캔 중...")
    symbols = get_binance_top_usdt(TOP_SCAN_LIMIT)
    await update.message.reply_text(build_compact_report(symbols, 15, True), parse_mode="HTML")

async def hot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 v16 HOT 후보 스캔 중...")
    symbols = get_binance_top_usdt(TOP_SCAN_LIMIT)
    results = scan(symbols, True)
    hot = [r for r in results if r.accumulation >= 55 and r.confidence >= 35 and r.bubble < 75 and r.distribution < 75]
    if not hot:
        await update.message.reply_text("HOT 후보 없음\n조건: 매집 55↑, 신뢰 35↑, 버블/분배 75↓")
        return
    await update.message.reply_text(format_compact_rank(hot, 10), parse_mode="HTML")

async def risk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(context.args).strip()
    symbols = [x.strip().upper() for x in raw.replace(" ", "").split(",") if x.strip()] if raw else DEFAULT_SYMBOLS
    await update.message.reply_text("A100 v16 위험 후보 점검 중...")
    results = scan(symbols, True)
    risky = sorted(results, key=lambda r: (r.bubble + r.distribution - r.confidence), reverse=True)
    lines = ["⚠ <b>A100 위험도 TOP</b>", ""]
    for i, r in enumerate(risky[:10], 1):
        verdict = "추격금지" if r.bubble >= 70 or r.distribution >= 70 else "주의"
        lines.append(
            f"{i}. <b>{r.pair}</b> | 버블 {r.bubble}% | 분배 {r.distribution}% | 신뢰 {r.confidence}%\n"
            f"판정: <b>{verdict}</b> | 가격 <code>{r.price}</code>"
        )
    await update.message.reply_text("\n\n".join(lines), parse_mode="HTML")


async def kr_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("업비트+빗썸 KRW 거래대금 확인 중...")
    await update.message.reply_text(build_kr_report(20), parse_mode="HTML")

async def cgtest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else "BTC"
    await update.message.reply_text(cg_test_text(symbol), parse_mode="HTML")

async def arkm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(build_report(["ARKM"], 1, True), parse_mode="HTML")

def send_telegram(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        log("BOT_TOKEN 또는 CHAT_ID 없음")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
                      timeout=15)
    except Exception as e:
        log(f"telegram send error: {e}")

def morning_job():
    send_telegram("🌅 <b>A100 오전 5시 v16 자동 리포트</b>\n\n" + build_report(DEFAULT_SYMBOLS, 10, True))

def alert_job():
    hits = [r for r in scan(DEFAULT_SYMBOLS, True) if r.score >= SCORE_ALERT or r.accumulation >= 80]
    if hits:
        send_telegram("🚨 <b>A100 v16 조건 감지</b>\n\n" + format_compact_rank(hits, 5))

def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN 필요")
    threading.Thread(target=start_health_server, daemon=True).start()

    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    scheduler.add_job(morning_job, CronTrigger(hour=5, minute=0))
    scheduler.add_job(alert_job, "interval", minutes=30)
    scheduler.start()

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("kr", kr_cmd))
    app.add_handler(CommandHandler("cgtest", cgtest_cmd))
    app.add_handler(CommandHandler("arkm", arkm))
    log("A100 v16 Fixed Ranker worker running...")
    app.run_polling()

if __name__ == "__main__":
    main()
