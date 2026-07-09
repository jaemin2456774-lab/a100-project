#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, requests
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
CG_KEY = os.getenv("COINGLASS_API_KEY", "").strip()
DEFAULT_SYMBOLS = [x.strip().upper() for x in os.getenv("DEFAULT_SYMBOLS", "ARKM,SYN,SENT,VANRY,ALT").split(",") if x.strip()]
SCORE_ALERT = float(os.getenv("SCORE_ALERT", "80"))

COINGLASS_BASE = "https://open-api-v4.coinglass.com"
BINANCE_FAPI = "https://fapi.binance.com"
BINANCE_SPOT = "https://api.binance.com"

def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x) if x is not None else default
    except Exception:
        return default

def pct(new: float, old: float) -> float:
    return 0.0 if old == 0 else (new - old) / abs(old) * 100.0

def grade(score: float) -> str:
    if score >= 95: return "S"
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "PASS"

def sma(values: List[float], n: int) -> Optional[float]:
    return sum(values[-n:]) / n if len(values) >= n else None

def avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def get_json(url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Any:
    r = requests.get(url, params=params or {}, headers=headers or {}, timeout=15)
    r.raise_for_status()
    return r.json()

def futures_klines(pair: str, interval: str = "4h", limit: int = 120) -> List[Dict[str, float]]:
    rows = get_json(f"{BINANCE_FAPI}/fapi/v1/klines", {"symbol": pair, "interval": interval, "limit": limit})
    return [{"open": safe_float(r[1]), "high": safe_float(r[2]), "low": safe_float(r[3]), "close": safe_float(r[4]), "quote_volume": safe_float(r[7])} for r in rows]

def spot_klines(pair: str, interval: str = "4h", limit: int = 80) -> Optional[List[Dict[str, float]]]:
    try:
        rows = get_json(f"{BINANCE_SPOT}/api/v3/klines", {"symbol": pair, "interval": interval, "limit": limit})
        return [{"close": safe_float(r[4]), "quote_volume": safe_float(r[7])} for r in rows]
    except Exception:
        return None

def funding(pair: str) -> float:
    try:
        rows = get_json(f"{BINANCE_FAPI}/fapi/v1/fundingRate", {"symbol": pair, "limit": 1})
        return safe_float(rows[-1].get("fundingRate")) * 100
    except Exception:
        return 0.0

def coinglass_data(path: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    if not CG_KEY:
        return None
    try:
        data = get_json(COINGLASS_BASE + path, params, {"CG-API-KEY": CG_KEY, "accept": "application/json"})
        d = data.get("data")
        return d if isinstance(d, list) and d else None
    except Exception:
        return None

@dataclass
class Result:
    pair: str
    price: float
    score: float
    grade: str
    trend: float
    oi: float
    funding_score: float
    volume: float
    spot_volume: float
    risk: float
    funding_pct: float
    oi_change_pct: float
    vol_ratio: float
    spot_vol_ratio: float
    note: str

def analyze(symbol: str, interval: str = "4h") -> Result:
    symbol = symbol.upper().replace("USDT", "")
    pair = f"{symbol}USDT"
    kl = futures_klines(pair, interval, 120)
    closes = [x["close"] for x in kl]
    lows = [x["low"] for x in kl]
    qvols = [x["quote_volume"] for x in kl]
    price = closes[-1]
    ma5, ma20, ma60 = sma(closes, 5) or price, sma(closes, 20) or price, sma(closes, 60) or price
    recent_low = min(lows[-30:])
    prev_low = min(lows[-60:-30]) if len(lows) >= 60 else recent_low

    trend = 0
    if price > ma5: trend += 5
    if price > ma20: trend += 7
    if ma5 > ma20: trend += 5
    if price > ma60: trend += 4
    if recent_low >= prev_low * 0.98: trend += 4

    vol_now = avg(qvols[-3:])
    vol_base = avg(qvols[-60:-15]) if len(qvols) >= 60 else avg(qvols[:-3])
    vol_ratio = vol_now / vol_base if vol_base else 1.0
    volume = min(max((vol_ratio - 1) * 10, 0), 20)

    spot_volume, spot_vol_ratio = 5, 1.0
    sk = spot_klines(pair, interval, 80)
    if sk and len(sk) >= 50:
        sq = [x["quote_volume"] for x in sk]
        s_now, s_base = avg(sq[-3:]), avg(sq[-50:-15])
        spot_vol_ratio = s_now / s_base if s_base else 1.0
        spot_volume = min(max((spot_vol_ratio - 1) * 10, 0), 15)

    fr = funding(pair)
    if -0.08 <= fr < -0.01: funding_score = 15
    elif -0.01 <= fr <= 0.02: funding_score = 12
    elif 0.02 < fr <= 0.05: funding_score = 7
    else: funding_score = 4

    oi_change, oi_score = 0.0, 8
    oid = coinglass_data("/api/futures/open-interest/aggregated-history", {"symbol": symbol, "interval": interval, "limit": 30, "unit": "usd"})
    if oid and len(oid) >= 6:
        oi_now = safe_float(oid[-1].get("close") or oid[-1].get("value"))
        oi_prev = safe_float(oid[-6].get("close") or oid[-6].get("value"))
        oi_change = pct(oi_now, oi_prev)
        oi_score = min(max(oi_change * 1.2, 0), 20)

    chg_24 = pct(closes[-1], closes[-7]) if interval == "4h" and len(closes) >= 7 else 0
    risk = 10
    if chg_24 > 40: risk -= 5
    if vol_ratio > 8 and chg_24 > 25: risk -= 3
    risk = max(risk, 0)

    score = trend + volume + spot_volume + funding_score + oi_score + risk
    notes = []
    if oi_change < 5: notes.append("OI 부족")
    if vol_ratio < 1.5: notes.append("선물 거래량 부족")
    if spot_vol_ratio < 1.5: notes.append("현물 거래량 부족")
    if price < ma20: notes.append("MA20 아래")
    if fr > 0.05: notes.append("펀딩 과열")

    return Result(pair, round(price,8), round(score,2), grade(score), round(trend,2), round(oi_score,2), round(funding_score,2), round(volume,2), round(spot_volume,2), round(risk,2), round(fr,4), round(oi_change,2), round(vol_ratio,2), round(spot_vol_ratio,2), " / ".join(notes) if notes else "양호")

def scan(symbols: List[str]) -> List[Result]:
    out = []
    for s in symbols:
        try: out.append(analyze(s))
        except Exception as e: print(f"{s} error: {e}")
        time.sleep(0.15)
    return sorted(out, key=lambda x: x.score, reverse=True)

def format_result(r: Result) -> str:
    return (f"📊 <b>{r.pair}</b>\n가격: <code>{r.price}</code>\n점수: <b>{r.score}</b> / 등급: <b>{r.grade}</b>\n"
            f"Funding: {r.funding_pct}% | OI: {r.oi_change_pct}%\n선물Vol: {r.vol_ratio}x | 현물Vol: {r.spot_vol_ratio}x\n"
            f"차트 {r.trend}/25 | OI {r.oi}/20 | Funding {r.funding_score}/15\n진단: {r.note}\n")

def build_report(symbols: List[str]) -> str:
    results = scan(symbols)
    if not results: return "A100 결과 없음"
    return "🔥 <b>A100 리포트</b>\n\n" + "\n---\n".join(format_result(r) for r in results[:10])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 봇 시작\n/check\n/scan ARKM,SYN,SENT\n/myid")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"TELEGRAM_CHAT_ID = {update.effective_chat.id}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A100 분석 중...")
    await update.message.reply_text(build_report(DEFAULT_SYMBOLS), parse_mode="HTML")

async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(context.args).strip()
    if not raw:
        await update.message.reply_text("예: /scan ARKM,SYN,SENT")
        return
    symbols = [x.strip().upper() for x in raw.replace(" ", "").split(",") if x.strip()]
    await update.message.reply_text("A100 분석 중...")
    await update.message.reply_text(build_report(symbols), parse_mode="HTML")

async def arkm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(build_report(["ARKM"]), parse_mode="HTML")

def send_telegram(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN 또는 CHAT_ID 없음")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
    except Exception as e:
        print("telegram send error:", e)

def morning_job():
    send_telegram("🌅 <b>A100 오전 5시 자동 리포트</b>\n\n" + build_report(DEFAULT_SYMBOLS))

def alert_job():
    hits = [r for r in scan(DEFAULT_SYMBOLS) if r.score >= SCORE_ALERT]
    if hits:
        send_telegram("🚨 <b>A100 조건 감지</b>\n\n" + "\n---\n".join(format_result(r) for r in hits[:5]))

def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN 필요")
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    scheduler.add_job(morning_job, CronTrigger(hour=5, minute=0))
    scheduler.add_job(alert_job, "interval", minutes=30)
    scheduler.start()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("arkm", arkm))
    print("A100 worker running...")
    app.run_polling()

if __name__ == "__main__":
    main()
