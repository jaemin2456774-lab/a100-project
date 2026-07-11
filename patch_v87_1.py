#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path

BLOCK = r"""
# ===== A100 v87.1 COMMAND FIX START =====
def _v871_symbol(args):
    raw = (args[0] if args else "BTC").upper().strip()
    raw = raw.replace("/", "").replace("-", "")
    if raw.endswith("USDT"):
        raw = raw[:-4]
    raw = re.sub(r"[^A-Z0-9]", "", raw)
    return raw or "BTC"

def _v871_snapshot(symbol):
    pair = symbol + "USDT"
    t = requests.get(
        "https://api.binance.com/api/v3/ticker/24hr",
        params={"symbol": pair}, timeout=8
    )
    if t.status_code >= 400:
        return None, f"{pair} 조회 실패 HTTP {t.status_code}"
    k = requests.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": pair, "interval": "4h", "limit": 60}, timeout=8
    )
    if k.status_code >= 400:
        return None, f"{pair} 캔들 조회 실패 HTTP {k.status_code}"

    ticker = t.json()
    rows = k.json()
    closes = [float(x[4]) for x in rows]
    highs = [float(x[2]) for x in rows]
    qv = [float(x[7]) for x in rows]
    tbq = [float(x[10]) for x in rows]

    price = closes[-1]
    ma5 = sum(closes[-5:]) / 5
    ma20 = sum(closes[-20:]) / 20
    vol_now = sum(qv[-3:]) / 3
    vol_base = sum(qv[-30:-3]) / max(1, len(qv[-30:-3]))
    vol_ratio = vol_now / vol_base if vol_base else 1.0
    buy_ratio = sum(tbq[-3:]) / max(sum(qv[-3:]), 1.0)
    chg24 = float(ticker.get("priceChangePercent", 0) or 0)
    high20 = max(highs[-20:])

    trend = 0.0
    trend += 25 if price > ma5 else 0
    trend += 25 if ma5 > ma20 else 0
    trend += 20 if price > ma20 else 0
    trend += min(15, max(0, (vol_ratio - 1) * 10))
    trend += min(15, max(0, (buy_ratio - 0.45) * 100))
    trend = max(0, min(100, trend))

    return {
        "pair": pair, "price": price, "ma5": ma5, "ma20": ma20,
        "vol_ratio": vol_ratio, "buy_ratio": buy_ratio,
        "chg24": chg24, "high20": high20, "trend": trend
    }, None

def _v871_bar(v, width=10):
    n = max(0, min(width, round(v / 100 * width)))
    return "█" * n + "░" * (width - n)

async def whale87_cmd(update, context):
    symbol = _v871_symbol(getattr(context, "args", []))
    try:
        d, err = await asyncio.to_thread(_v871_snapshot, symbol)
        if not d:
            await update.message.reply_text("⚠️ /whale87 오류\n" + str(err))
            return

        buy = d["buy_ratio"] * 100
        score = (
            d["trend"] * 0.45
            + min(100, d["vol_ratio"] * 35) * 0.30
            + max(0, min(100, (buy - 40) * 4)) * 0.25
        )
        score = max(0, min(100, score))

        if score >= 75:
            verdict = "🟢 매집 우세"
        elif score >= 58:
            verdict = "🟡 매집 관찰"
        elif score >= 42:
            verdict = "⚪ 중립"
        else:
            verdict = "🔴 분배/약세 주의"

        await update.message.reply_text(
            f"🐋 A100 v87.1 세력 흐름\n"
            f"종목: {d['pair']}\n"
            f"판정: {verdict}\n\n"
            f"세력 점수: {score:.1f}/100\n"
            f"{_v871_bar(score)}\n"
            f"Taker 매수비율: {buy:.1f}%\n"
            f"거래량 배율: {d['vol_ratio']:.2f}x\n"
            f"24시간 변화: {d['chg24']:+.2f}%\n"
            f"추세 점수: {d['trend']:.1f}/100\n\n"
            f"※ 공개 시장 데이터 기반 추정치입니다."
        )
        print(f"v87.1 whale87 ok {d['pair']}", flush=True)
    except Exception as e:
        print(f"v87.1 whale87 error {e}", flush=True)
        await update.message.reply_text(f"⚠️ /whale87 처리 오류: {type(e).__name__}")

async def alertplan_cmd(update, context):
    symbol = _v871_symbol(getattr(context, "args", []))
    try:
        d, err = await asyncio.to_thread(_v871_snapshot, symbol)
        if not d:
            await update.message.reply_text("⚠️ /alertplan 오류\n" + str(err))
            return

        buy = d["buy_ratio"] * 100
        near_high = d["price"] / d["high20"] * 100 if d["high20"] else 0
        checks = [
            ("추세", d["price"] > d["ma20"]),
            ("단기 정배열", d["ma5"] > d["ma20"]),
            ("거래량 1.5배", d["vol_ratio"] >= 1.5),
            ("Taker 매수 우위", buy >= 52),
            ("20봉 고점 접근", near_high >= 97),
            ("24h 과열 아님", d["chg24"] < 20),
        ]
        passed = sum(1 for _, ok in checks if ok)
        confidence = max(0, min(100,
            d["trend"] * 0.55
            + min(100, d["vol_ratio"] * 32) * 0.25
            + max(0, min(100, (buy - 40) * 4)) * 0.20
        ))

        if confidence >= 75 and passed >= 5:
            action = "🟢 조건부 진입 감시"
        elif confidence >= 58 and passed >= 3:
            action = "🟡 대기 후 재확인"
        else:
            action = "🔴 진입 금지"

        checklist = "\n".join(
            f"{'✅' if ok else '⬜'} {name}" for name, ok in checks
        )
        await update.message.reply_text(
            f"🔔 A100 v87.1 알림 계획\n"
            f"종목: {d['pair']}\n"
            f"현재 행동: {action}\n"
            f"신뢰도: {confidence:.1f}%\n"
            f"충족 조건: {passed}/{len(checks)}\n\n"
            f"{checklist}\n\n"
            f"재확인 조건\n"
            f"• 거래량 1.5배 이상\n"
            f"• Taker 매수비율 52% 이상\n"
            f"• MA5 > MA20 유지\n"
            f"• 24시간 급등 20% 미만\n\n"
            f"※ 주문 실행 명령이 아니라 감시 계획입니다."
        )
        print(f"v87.1 alertplan ok {d['pair']}", flush=True)
    except Exception as e:
        print(f"v87.1 alertplan error {e}", flush=True)
        await update.message.reply_text(f"⚠️ /alertplan 처리 오류: {type(e).__name__}")
# ===== A100 v87.1 COMMAND FIX END =====
"""

def patch(path: Path):
    src = path.read_text(encoding="utf-8")
    backup = path.with_suffix(path.suffix + ".v87_backup")
    backup.write_text(src, encoding="utf-8")

    src = re.sub(
        r"# ===== A100 v87\.1 COMMAND FIX START =====.*?# ===== A100 v87\.1 COMMAND FIX END =====\n?",
        "",
        src,
        flags=re.S,
    )

    marker = "def build_v44_application(token):"
    if marker not in src:
        raise SystemExit("build_v44_application(token) 함수를 찾지 못했습니다.")

    src = src.replace(marker, BLOCK + "\n\n" + marker, 1)

    # handlers 리스트에 두 명령 등록
    pat = r'(\("datastatus",\s*datastatus_cmd\)\s*\])'
    if re.search(pat, src):
        src = re.sub(
            pat,
            '("datastatus", datastatus_cmd),\n'
            '        ("whale87", whale87_cmd),\n'
            '        ("alertplan", alertplan_cmd)]',
            src,
            count=1,
        )
    else:
        raise SystemExit("handlers 리스트 끝부분을 찾지 못했습니다.")

    # 시작 문구 교체
    src = re.sub(
        r'print\("A100 v[^"]*worker running\.\.\.", flush=True\)',
        'print("A100 v87.1 SIGNAL PULSE worker running...", flush=True)',
        src,
        count=1,
    )

    path.write_text(src, encoding="utf-8")
    print(f"완료: {path}")
    print(f"백업: {backup}")
    print("등록 명령: /whale87 [심볼], /alertplan [심볼]")
    print("예: /whale87 BTC  /alertplan BTC")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("사용법: python patch_v87_1.py main.py")
    patch(Path(sys.argv[1]))
