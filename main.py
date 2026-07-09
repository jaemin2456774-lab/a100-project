#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    "BTC,ETH,SOL,ARKM,SYN,SENT,ALT,VANRY,CELO,COTI,NFP,TIA,INJ,WLD,ZEC"
).split(",") if x.strip()]
SCORE_ALERT = float(os.getenv("SCORE_ALERT", "80"))

BINANCE_MARKET = "https://data-api.binance.vision"
UPBIT = "https://api.upbit.com"
BITHUMB = "https://api.bithumb.com"
CG_BASE = "https://open-api-v4.coinglass.com"

def log(msg: str):
    print(msg, flush=True)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"A100 v11 CoinGlass KR worker is running"
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

def get_json(url: str, params=None, headers=None):
    r = requests.get(url, params=params or {}, headers=headers or {}, timeout=15)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} {url} {r.text[:200]}")
    return r.json()

def grade(score: float) -> str:
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "PASS"

# ---------- CoinGlass ----------
def cg_get(path: str, params: Dict[str, Any]) -> Optional[Any]:
    if not CG_KEY:
        log("CoinGlass key empty")
        return None
    try:
        data = get_json(CG_BASE + path, params, {"CG-API-KEY": CG_KEY, "accept": "application/json"})
        if "data" not in data:
            log(f"CoinGlass no data field: {path} {str(data)[:180]}")
            return None
        return data["data"]
    except Exception as e:
        log(f"CoinGlass error {path} {params}: {e}")
        return None

def cg_rows(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        # Some endpoints may return {"list":[...]} or exchange map
        for key in ["list", "data", "rows"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        return [data]
    return []

def cg_last_num(row: Dict[str, Any], keys: List[str], default=0.0) -> float:
    for k in keys:
        if k in row:
            return safe_float(row.get(k), default)
    return default

def cg_oi_change(symbol: str, interval="4h") -> Tuple[float, float, str]:
    data = cg_get("/api/futures/open-interest/aggregated-history", {
        "symbol": symbol, "interval": interval, "limit": 30, "unit": "usd"
    })
    rows = cg_rows(data)
    if len(rows) >= 6:
        now = cg_last_num(rows[-1], ["close", "value", "openInterest", "sumOpenInterest"], 0)
        prev = cg_last_num(rows[-6], ["close", "value", "openInterest", "sumOpenInterest"], 0)
        chg = pct(now, prev)
        score = min(max(chg * 1.2, 0), 15)
        return score, chg, "CG OI"
    return 0.0, 0.0, "CG OI 없음"

def cg_funding(symbol: str, interval="4h") -> Tuple[float, float, str]:
    data = cg_get("/api/futures/funding-rate/oi-weight-history", {
        "symbol": symbol, "interval": interval, "limit": 10
    })
    rows = cg_rows(data)
    rate = 0.0
    if rows:
        row = rows[-1]
        rate = cg_last_num(row, ["close", "rate", "fundingRate", "value"], 0)
        # If raw fraction, convert to percent
        if abs(rate) < 1:
            rate *= 100
    # Negative/neutral funding is better for long squeeze candidate
    if -0.08 <= rate < -0.01: score = 10
    elif -0.01 <= rate <= 0.02: score = 8
    elif 0.02 < rate <= 0.05: score = 4
    else: score = 2
    return score, round(rate, 5), "CG Funding" if rows else "CG Funding 없음"

def cg_taker_ratio(symbol: str, interval="4h") -> Tuple[float, float, str]:
    data = cg_get("/api/futures/aggregated-taker-buy-sell-volume/history", {
        "symbol": symbol, "interval": interval, "limit": 10
    })
    rows = cg_rows(data)
    if rows:
        row = rows[-1]
        buy = cg_last_num(row, ["buy", "buyVolume", "takerBuyVol", "takerBuyVolume"], 0)
        sell = cg_last_num(row, ["sell", "sellVolume", "takerSellVol", "takerSellVolume"], 0)
        ratio = buy / sell if sell else 1.0
        if 0.85 <= ratio <= 1.35: score = 5
        elif 1.35 < ratio <= 2.0: score = 4
        elif 0.65 <= ratio < 0.85: score = 3
        else: score = 1
        return score, round(ratio, 3), "CG Taker"
    return 0.0, 0.0, "CG Taker 없음"

def cg_snapshot(symbol: str) -> Dict[str, Any]:
    oi_s, oi_chg, oi_note = cg_oi_change(symbol)
    fund_s, fund_rate, fund_note = cg_funding(symbol)
    taker_s, taker_ratio, taker_note = cg_taker_ratio(symbol)
    return {
        "oi_score": oi_s,
        "oi_change": oi_chg,
        "oi_note": oi_note,
        "funding_score": fund_s,
        "funding_rate": fund_rate,
        "funding_note": fund_note,
        "taker_score": taker_s,
        "taker_ratio": taker_ratio,
        "taker_note": taker_note,
        "total": oi_s + fund_s + taker_s,
    }

def cg_test_text(symbol="BTC") -> str:
    snap = cg_snapshot(symbol.upper().replace("USDT", ""))
    return (
        f"🧪 <b>CoinGlass 테스트 {symbol.upper()}</b>\n"
        f"OI 변화: {snap['oi_change']}% / 점수 {snap['oi_score']} ({snap['oi_note']})\n"
        f"Funding: {snap['funding_rate']}% / 점수 {snap['funding_score']} ({snap['funding_note']})\n"
        f"Taker: {snap['taker_ratio']} / 점수 {snap['taker_score']} ({snap['taker_note']})"
    )

# ---------- Binance market data ----------
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

def get_binance_top_usdt(limit: int = 40) -> List[str]:
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

# ---------- Korean markets ----------
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

def kr_score_for_symbol(sym: str, kr: Dict[str, Dict[str, float]]) -> Tuple[float, str]:
    x = kr.get(sym.upper())
    if not x:
        return 0.0, "국내 미상장/데이터 없음"
    value = x.get("kr_value", 0)
    chg = x.get("kr_change", 0)
    score = 0
    if value >= 10_000_000_000: score += 4
    if value >= 30_000_000_000: score += 4
    if value >= 100_000_000_000: score += 4
    if chg > 2: score += 3
    if chg > 5: score += 3
    score = min(score, 15)
    return score, f"KR거래대금 {value/100000000:.1f}억 / KR등락 {chg:.2f}%"

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
    kr_note: str
    note: str

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

    chart = 0
    if price > ma5: chart += 6
    if price > ma20: chart += 7
    if ma5 > ma20: chart += 5
    if price > ma60: chart += 4
    if recent_low >= prev_low * 0.98: chart += 3
    chart = min(chart, 25)

    vol_now = avg(qvols[-3:])
    vol_base = avg(qvols[-60:-15])
    vol_ratio = vol_now / vol_base if vol_base else 1.0
    volume = min(max((vol_ratio - 1) * 8, 0), 15)

    buy_now = avg(buyq[-3:])
    buy_ratio = buy_now / vol_now if vol_now else 0.5
    if buy_ratio > 0.60: volume += 5
    elif buy_ratio > 0.56: volume += 4
    elif buy_ratio > 0.52: volume += 2
    volume = min(volume, 20)

    rsi14 = rsi(closes, 14)
    mh = macd_hist(closes)
    momentum = 0
    if 45 <= rsi14 <= 68: momentum += 2
    if mh > 0: momentum += 2
    if closes[-1] > closes[-4]: momentum += 1

    kr = kr or {}
    kr_score, kr_note = kr_score_for_symbol(symbol, kr)

    cg = cg_snapshot(symbol)
    cg_score = min(cg["total"], 30)
    cg_text = f"OI {cg['oi_change']}% / Funding {cg['funding_rate']}% / Taker {cg['taker_ratio']}"

    chg_24 = pct(closes[-1], closes[-7])
    risk = 10
    if chg_24 > 25: risk -= 3
    if chg_24 > 45: risk -= 4
    if price < ma20: risk -= 3
    risk = max(risk, 0)

    score = chart + volume + kr_score + cg_score + momentum + risk

    notes = []
    if cg["oi_score"] >= 8: notes.append("OI 증가 감지")
    if cg["funding_score"] >= 8: notes.append("펀딩 양호")
    if vol_ratio < 1.5: notes.append("글로벌 거래량 부족")
    if buy_ratio < 0.52: notes.append("글로벌 매수압 약함")
    if price < ma20: notes.append("MA20 아래")
    if mh <= 0: notes.append("MACD 약함")
    if kr_score >= 8: notes.append("국내 현물 수급")
    if chg_24 > 35: notes.append("단기 급등 리스크")
    if not notes: notes.append("A100 조건 양호")

    result = Result(
        pair, round(price, 8), round(score, 2), grade(score),
        round(chart, 2), round(volume, 2), round(kr_score, 2),
        round(cg_score, 2), round(momentum, 2), round(risk, 2),
        round(vol_ratio, 2), round(buy_ratio, 3), round(rsi14, 2),
        round(support, 8), round(resistance, 8),
        cg_text, kr_note, " / ".join(notes)
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

def format_result(r: Result) -> str:
    return (
        f"📊 <b>{r.pair}</b>\n"
        f"가격: <code>{r.price}</code>\n"
        f"점수: <b>{r.score}</b> / 등급: <b>{r.grade}</b>\n"
        f"지지: <code>{r.support}</code> | 저항: <code>{r.resistance}</code>\n"
        f"Vol: {r.vol_ratio}x | 매수비율: {r.buy_ratio} | RSI: {r.rsi14}\n"
        f"점수구성: 차트 {r.chart_score}/25 | 거래량 {r.volume_score}/20 | KR {r.kr_score}/15 | CG {r.cg_score}/30 | 모멘텀 {r.momentum_score}/5 | 리스크 {r.risk_score}/10\n"
        f"CG: {r.cg_text}\n"
        f"{r.kr_note}\n"
        f"진단: {r.note}\n"
    )

def build_report(symbols: List[str], top_n: int = 10, use_kr: bool = True) -> str:
    results = scan(symbols, use_kr=use_kr)
    if not results:
        return "A100 결과 없음\n\nRender 로그 error 확인 필요"
    return "🔥 <b>A100 v11 CoinGlass+KR 리포트</b>\n\n" + "\n---\n".join(format_result(r) for r in results[:top_n])

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 봇 시작\n/check\n/scan ARKM,SYN,SENT\n/top\n/kr\n/cgtest BTC\n/myid")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"TELEGRAM_CHAT_ID = {update.effective_chat.id}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 v11 CoinGlass+KR 기본 리스트 분석 중...")
    await update.message.reply_text(build_report(DEFAULT_SYMBOLS, 10, True), parse_mode="HTML")

async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(context.args).strip()
    if not raw:
        await update.message.reply_text("예: /scan ARKM,SYN,SENT")
        return
    symbols = [x.strip().upper() for x in raw.replace(" ", "").split(",") if x.strip()]
    await update.message.reply_text("A100 v11 CoinGlass+KR 분석 중...")
    await update.message.reply_text(build_report(symbols, 10, True), parse_mode="HTML")

async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 거래량 상위 USDT 40개 + CoinGlass + 국내수급 스캔 중...")
    symbols = get_binance_top_usdt(40)
    await update.message.reply_text(build_report(symbols, 10, True), parse_mode="HTML")

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
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
    except Exception as e:
        log(f"telegram send error: {e}")

def morning_job():
    send_telegram("🌅 <b>A100 오전 5시 CoinGlass+KR 자동 리포트</b>\n\n" + build_report(DEFAULT_SYMBOLS, 10, True))

def alert_job():
    hits = [r for r in scan(DEFAULT_SYMBOLS, True) if r.score >= SCORE_ALERT]
    if hits:
        send_telegram("🚨 <b>A100 조건 감지</b>\n\n" + "\n---\n".join(format_result(r) for r in hits[:5]))

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
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("kr", kr_cmd))
    app.add_handler(CommandHandler("cgtest", cgtest_cmd))
    app.add_handler(CommandHandler("arkm", arkm))
    log("A100 v11 CoinGlass KR worker running...")
    app.run_polling()

if __name__ == "__main__":
    main()
