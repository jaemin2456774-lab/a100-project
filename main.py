#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, requests, asyncio, threading, traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
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
DEFAULT_SYMBOLS = [x.strip().upper() for x in os.getenv("DEFAULT_SYMBOLS", "BTC,ETH,SOL,ARKM,SYN,SENT").split(",") if x.strip()]
SCORE_ALERT = float(os.getenv("SCORE_ALERT", "80"))

BINANCE_SPOT = "https://api.binance.com"

def log(msg: str):
    print(msg, flush=True)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"A100 spot-only worker is running"
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

def grade(score: float) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "PASS"

def avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def sma(values: List[float], n: int) -> Optional[float]:
    return sum(values[-n:]) / n if len(values) >= n else None

def get_json(url: str, params=None):
    r = requests.get(url, params=params or {}, timeout=15)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} {url} {r.text[:120]}")
    return r.json()

def get_spot_klines(pair: str, interval: str = "4h", limit: int = 120) -> List[Dict[str, float]]:
    rows = get_json(f"{BINANCE_SPOT}/api/v3/klines", {"symbol": pair, "interval": interval, "limit": limit})
    return [{
        "open": safe_float(r[1]),
        "high": safe_float(r[2]),
        "low": safe_float(r[3]),
        "close": safe_float(r[4]),
        "quote_volume": safe_float(r[7]),
        "trades": safe_float(r[8]),
        "taker_buy_quote": safe_float(r[10]),
    } for r in rows]

@dataclass
class Result:
    pair: str
    price: float
    score: float
    grade: str
    trend: float
    volume: float
    buy_pressure: float
    risk: float
    vol_ratio: float
    buy_ratio: float
    note: str

def analyze(symbol: str, interval: str = "4h") -> Result:
    symbol = symbol.upper().replace("USDT", "")
    pair = f"{symbol}USDT"
    log(f"SPOT analyze start: {pair}")

    kl = get_spot_klines(pair, interval, 120)
    closes = [x["close"] for x in kl]
    lows = [x["low"] for x in kl]
    qvols = [x["quote_volume"] for x in kl]
    buyq = [x["taker_buy_quote"] for x in kl]
    price = closes[-1]

    ma5 = sma(closes, 5) or price
    ma20 = sma(closes, 20) or price
    ma60 = sma(closes, 60) or price
    recent_low = min(lows[-30:])
    prev_low = min(lows[-60:-30]) if len(lows) >= 60 else recent_low

    trend = 0
    if price > ma5: trend += 8
    if price > ma20: trend += 10
    if ma5 > ma20: trend += 7
    if price > ma60: trend += 6
    if recent_low >= prev_low * 0.98: trend += 6
    trend = min(trend, 35)

    vol_now = avg(qvols[-3:])
    vol_base = avg(qvols[-60:-15]) if len(qvols) >= 60 else avg(qvols[:-3])
    vol_ratio = vol_now / vol_base if vol_base else 1.0
    volume = min(max((vol_ratio - 1) * 12, 0), 25)

    buy_now = avg(buyq[-3:])
    buy_ratio = buy_now / vol_now if vol_now else 0.5
    buy_pressure = 0
    if buy_ratio > 0.52: buy_pressure += 8
    if buy_ratio > 0.56: buy_pressure += 7
    if buy_ratio > 0.60: buy_pressure += 5

    chg_24 = pct(closes[-1], closes[-7]) if len(closes) >= 7 else 0
    risk = 20
    if chg_24 > 25: risk -= 6
    if chg_24 > 45: risk -= 8
    if price < ma20: risk -= 5
    risk = max(risk, 0)

    score = trend + volume + buy_pressure + risk

    notes = []
    if vol_ratio < 1.5: notes.append("거래량 부족")
    if buy_ratio < 0.52: notes.append("매수압 약함")
    if price < ma20: notes.append("MA20 아래")
    if chg_24 > 35: notes.append("단기 급등 리스크")
    if not notes: notes.append("현물 구조 양호")

    result = Result(pair, round(price, 8), round(score, 2), grade(score), round(trend, 2), round(volume, 2), round(buy_pressure, 2), round(risk, 2), round(vol_ratio, 2), round(buy_ratio, 3), " / ".join(notes))
    log(f"SPOT analyze done: {pair} score={result.score}")
    return result

def scan(symbols: List[str]) -> List[Result]:
    log(f"scan symbols={symbols}")
    out = []
    for s in symbols:
        try:
            out.append(analyze(s))
        except Exception as e:
            log(f"{s} error: {e}")
            log(traceback.format_exc())
        time.sleep(0.15)
    return sorted(out, key=lambda x: x.score, reverse=True)

def format_result(r: Result) -> str:
    return (
        f"📊 <b>{r.pair}</b>\n"
        f"가격: <code>{r.price}</code>\n"
        f"점수: <b>{r.score}</b> / 등급: <b>{r.grade}</b>\n"
        f"거래량: {r.vol_ratio}x | 매수비율: {r.buy_ratio}\n"
        f"차트 {r.trend}/35 | 거래량 {r.volume}/25 | 매수압 {r.buy_pressure}/20 | 리스크 {r.risk}/20\n"
        f"진단: {r.note}\n"
    )

def build_report(symbols: List[str]) -> str:
    results = scan(symbols)
    if not results:
        return "A100 결과 없음\n\nBinance Spot에서도 데이터 실패. Render 로그 error 확인 필요"
    return "🔥 <b>A100 Spot 리포트</b>\n\n" + "\n---\n".join(format_result(r) for r in results[:10])

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
        log("BOT_TOKEN 또는 CHAT_ID 없음")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
    except Exception as e:
        log(f"telegram send error: {e}")

def morning_job():
    send_telegram("🌅 <b>A100 오전 5시 자동 리포트</b>\n\n" + build_report(DEFAULT_SYMBOLS))

def alert_job():
    hits = [r for r in scan(DEFAULT_SYMBOLS) if r.score >= SCORE_ALERT]
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
    app.add_handler(CommandHandler("arkm", arkm))
    log("A100 spot-only worker running...")
    app.run_polling()

if __name__ == "__main__":
    main()
