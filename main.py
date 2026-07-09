
import os, time, asyncio, threading, traceback, requests
from dataclasses import dataclass
from typing import Any, Dict, List
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

# ===== A100 v30 안정화: API 캐시 / 레이트리밋 / 매크로 리스크 =====
import time as _a100_time

CG_CACHE = {}
CG_LAST_CALL = 0.0
CG_MIN_INTERVAL = float(os.getenv("CG_MIN_INTERVAL", "0.45"))
CG_CACHE_TTL = int(os.getenv("CG_CACHE_TTL", "300"))

def now_ts():
    return _a100_time.time()

def cg_symbol(sym):
    s = (sym or "").upper().replace("/", "").replace("-", "")
    if s.endswith("USDT"):
        return s[:-4]
    if s.endswith("USDC"):
        return s[:-4]
    return s

def cache_get(key, ttl=CG_CACHE_TTL):
    item = CG_CACHE.get(key)
    if not item:
        return None
    ts, val = item
    if now_ts() - ts <= ttl:
        return val
    return None

def cache_set(key, val):
    CG_CACHE[key] = (now_ts(), val)
    return val

def cg_rate_sleep():
    global CG_LAST_CALL
    gap = now_ts() - CG_LAST_CALL
    if gap < CG_MIN_INTERVAL:
        _a100_time.sleep(CG_MIN_INTERVAL - gap)
    CG_LAST_CALL = now_ts()

def safe_num(x, default=0.0):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def macro_risk_score():
    # 완전한 뉴스 크롤링 대신 Render 안정성을 위해 일정/키워드 기반 수동 입력 지원
    # Render Environment에 MACRO_RISK=0~100, MACRO_NOTE="FOMC D-1" 형태로 넣으면 추천 기준에 반영
    risk = safe_num(os.getenv("MACRO_RISK", "35"), 35)
    note = os.getenv("MACRO_NOTE", "수동 매크로 입력 없음")
    fomc = safe_num(os.getenv("FOMC_DAYS", "99"), 99)
    cpi = safe_num(os.getenv("CPI_DAYS", "99"), 99)
    war = safe_num(os.getenv("WAR_RISK", "0"), 0)
    if fomc <= 1:
        risk += 18
    elif fomc <= 3:
        risk += 10
    if cpi <= 1:
        risk += 15
    elif cpi <= 3:
        risk += 8
    risk += min(war, 25)
    return round(max(0, min(100, risk)), 1), note, fomc, cpi, war

def macro_guard_add():
    risk, *_ = macro_risk_score()
    if risk >= 75:
        return 12
    if risk >= 60:
        return 8
    if risk >= 45:
        return 4
    return 0

def macro_text():
    risk, note, fomc, cpi, war = macro_risk_score()
    if risk >= 75:
        level = "🔴 매우 높음"
    elif risk >= 60:
        level = "🟠 높음"
    elif risk >= 45:
        level = "🟡 보통"
    else:
        level = "🟢 낮음"
    return (
        f"🌎 <b>A100 v30 매크로 리스크</b>\n"
        f"위험도: <b>{risk}%</b> {level}\n"
        f"FOMC D-{int(fomc) if fomc < 90 else '?'} | CPI D-{int(cpi) if cpi < 90 else '?'} | 전쟁위험 {war}%\n"
        f"메모: {note}\n"
        f"판정: {'고배율 금지 / 알트 보수적' if risk >= 60 else '일반 기준 적용'}"
    )

BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN","").strip()
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID","").strip()
CG_KEY=os.getenv("COINGLASS_API_KEY","").strip()
DEFAULT_SYMBOLS=[x.strip().upper() for x in os.getenv("DEFAULT_SYMBOLS","BTC,ETH,SOL,ARKM,SYN,SENT,ALT,VANRY,CELO,COTI,NFP,TIA,INJ,WLD,ZEC").split(",") if x.strip()]
SCORE_ALERT=float(os.getenv("SCORE_ALERT","85"))
TOP_SCAN_LIMIT=int(os.getenv("TOP_SCAN_LIMIT","25"))
BINANCE="https://data-api.binance.vision"; UPBIT="https://api.upbit.com"; BITHUMB="https://api.bithumb.com"; CG="https://open-api-v4.coinglass.com"
CG_CACHE={}; KR_CACHE=(0,{})

def log(x): print(x, flush=True)
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        b=b"A100 v30 Korean News Meta AI running"; self.send_response(200); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self,*a): return
def health(): HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), Health).serve_forever()
def sf(x,d=0.0):
    try: return float(x) if x is not None else d
    except: return d
def avg(v): return sum(v)/len(v) if v else 0.0
def pct(a,b): return 0.0 if b==0 else (a-b)/abs(b)*100
def clamp(x,a=0,b=100): return max(a,min(b,x))
def sma(v,n): return avg(v[-n:]) if len(v)>=n else (v[-1] if v else 0)
def http(url,params=None,headers=None):
    r=requests.get(url,params=params or {},headers=headers or {},timeout=15)
    if r.status_code>=400: raise RuntimeError(f"HTTP {r.status_code} {url} {r.text[:120]}")
    return r.json()
def rsi(c,n=14):
    if len(c)<=n+1: return 50
    g=[]; l=[]
    for i in range(-n,0):
        d=c[i]-c[i-1]; g.append(max(d,0)); l.append(abs(min(d,0)))
    al=avg(l)
    if al==0: return 100
    rs=avg(g)/al; return 100-(100/(1+rs))
def ema(v,n):
    if not v: return []
    k=2/(n+1); o=[v[0]]
    for x in v[1:]: o.append(x*k+o[-1]*(1-k))
    return o
def macd(c):
    if len(c)<40: return 0
    e12=ema(c,12); e26=ema(c,26); m=[a-b for a,b in zip(e12[-len(e26):],e26)]; s=ema(m,9); return m[-1]-s[-1]
def atr(h,l,c,n=14):
    if len(c)<n+1: return 0
    return avg([max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(-n,0)])
def bar(v,w=10):
    f=int(round(clamp(v)/100*w)); return "■"*f+"□"*(w-f)
def stars(v):
    return "★★★★★" if v>=85 else "★★★★☆" if v>=70 else "★★★☆☆" if v>=55 else "★★☆☆☆" if v>=40 else "★☆☆☆☆"
def grade(v):
    return "S" if v>=92 else "A+" if v>=85 else "A" if v>=78 else "B" if v>=70 else "C" if v>=60 else "PASS"

def klines(sym):
    pair=sym.upper().replace("USDT","")+"USDT"
    rows=http(f"{BINANCE}/api/v3/klines",{"symbol":pair,"interval":"4h","limit":120})
    return [{"h":sf(r[2]),"l":sf(r[3]),"c":sf(r[4]),"qv":sf(r[7]),"tbq":sf(r[10])} for r in rows]
def top_usdt(n=25):
    data=http(f"{BINANCE}/api/v3/ticker/24hr")
    arr=[]
    for x in data:
        s=x.get("symbol","")
        if s.endswith("USDT") and not any(b in s for b in ["UPUSDT","DOWNUSDT","BULLUSDT","BEARUSDT"]):
            arr.append((s.replace("USDT",""),sf(x.get("quoteVolume"))))
    arr.sort(key=lambda x:x[1],reverse=True); return [x[0] for x in arr[:n]]

def cg_raw(path,params):
    if not CG_KEY: return None
    key=path+str(sorted(params.items())); now=time.time()
    if key in CG_CACHE and now-CG_CACHE[key][0]<180: return CG_CACHE[key][1]
    time.sleep(0.15)
    try:
        d=http(CG+path,params,{"CG-API-KEY":CG_KEY,"accept":"application/json"})
        if "data" in d: CG_CACHE[key]=(now,d["data"]); return d["data"]
        log(f"CG no data {path} {d}")
    except Exception as e: log(f"CG err {path} {e}")
    return None
def rows(d):
    if isinstance(d,list): return [x for x in d if isinstance(x,dict)]
    if isinstance(d,dict):
        for k in ["list","data","rows","items"]:
            if isinstance(d.get(k),list): return [x for x in d[k] if isinstance(x,dict)]
        return [d]
    return []
def val(r,ks):
    for k in ks:
        if k in r: return sf(r.get(k))
    return 0
def cg_snap(sym):
    sym=sym.upper().replace("USDT","")
    out={"oi":0,"oi_score":0,"fund":0,"fund_score":0,"taker":0,"taker_score":0,"ls":0,"ls_score":0,"liq_score":0,"liq":"청산데이터 없음"}
    d=rows(cg_raw("/api/futures/open-interest/aggregated-history",{"symbol":sym,"interval":"4h","limit":30,"unit":"usd"}))
    if len(d)>=6:
        o=val(d[-1],["close","value","openInterest","sumOpenInterest"]); p=val(d[-6],["close","value","openInterest","sumOpenInterest"])
        out["oi"]=round(pct(o,p),2); out["oi_score"]=min(max(out["oi"],0),15)
    d=rows(cg_raw("/api/futures/funding-rate/oi-weight-history",{"symbol":sym,"interval":"4h","limit":10}))
    if d:
        f=val(d[-1],["close","rate","fundingRate","value"])
        if abs(f)<1: f*=100
        out["fund"]=round(f,5); out["fund_score"]=10 if -0.08<=f< -0.01 else 8 if -0.01<=f<=0.02 else 3 if f<=0.05 else 1
    d=rows(cg_raw("/api/futures/aggregated-taker-buy-sell-volume/history",{"symbol":sym,"interval":"4h","limit":10}))
    if d:
        buy=val(d[-1],["buy","buyVolume","takerBuyVol","takerBuyVolume"]); sell=val(d[-1],["sell","sellVolume","takerSellVol","takerSellVolume"])
        ratio=buy/sell if sell else 1; out["taker"]=round(ratio,3); out["taker_score"]=5 if 0.85<=ratio<=1.35 else 4 if ratio<=2 else 1
    for path in ["/api/futures/global-long-short-account-ratio/history","/api/futures/top-long-short-account-ratio/history"]:
        d=rows(cg_raw(path,{"symbol":sym,"interval":"4h","limit":10}))
        if d:
            ratio=val(d[-1],["longShortRatio","ratio","longShortRate"]); out["ls"]=round(ratio,3); out["ls_score"]=3 if ratio and 0.6<=ratio<=1.15 else 2 if ratio and ratio<=1.6 else 1; break
    d=rows(cg_raw("/api/futures/liquidation/history",{"symbol":sym,"exchange":"Binance","interval":"4h","limit":12}))
    if d:
        ll=sl=0
        for r in d[-6:]:
            ll+=val(r,["longLiquidation","longLiquidationUsd","longVolUsd","long"]); sl+=val(r,["shortLiquidation","shortLiquidationUsd","shortVolUsd","short"])
        if sl>ll*1.5 and sl>0: out["liq_score"]=5; bias="상방 숏청산 우세"
        elif ll>sl*1.5 and ll>0: out["liq_score"]=1; bias="하방 롱청산 위험"
        else: out["liq_score"]=3; bias="청산 중립"
        out["liq"]=f"{bias} L:{ll:.0f} S:{sl:.0f}"
    out["cg_score"]=min((out["oi_score"]+out["fund_score"]+out["taker_score"]+out["ls_score"]+out["liq_score"])*35/38,35)
    return out

def kr_data():
    global KR_CACHE
    now=time.time()
    if now-KR_CACHE[0]<180 and KR_CACHE[1]: return KR_CACHE[1]
    res={}
    try:
        mk=http(f"{UPBIT}/v1/market/all",{"isDetails":"false"})
        krw=[x["market"] for x in mk if x.get("market","").startswith("KRW-")]
        for i in range(0,len(krw),100):
            d=http(f"{UPBIT}/v1/ticker",{"markets":",".join(krw[i:i+100])})
            for x in d:
                s=x["market"].replace("KRW-",""); res.setdefault(s,{})
                res[s]["uv"]=sf(x.get("acc_trade_price_24h")); res[s]["uc"]=sf(x.get("signed_change_rate"))*100
            time.sleep(0.05)
    except Exception as e: log(f"upbit {e}")
    try:
        d=http(f"{BITHUMB}/public/ticker/ALL_KRW").get("data",{})
        for s,x in d.items():
            if s=="date" or not isinstance(x,dict): continue
            res.setdefault(s.upper(),{}); res[s.upper()]["bv"]=sf(x.get("acc_trade_value_24H")); res[s.upper()]["bc"]=sf(x.get("fluctate_rate_24H"))
    except Exception as e: log(f"bithumb {e}")
    for s,x in res.items():
        x["v"]=sf(x.get("uv"))+sf(x.get("bv")); ch=[]
        if "uc" in x: ch.append(x["uc"])
        if "bc" in x: ch.append(x["bc"])
        x["c"]=avg(ch)
    KR_CACHE=(now,res); return res
def kr_score(sym,kr):
    x=kr.get(sym.upper().replace("USDT",""),{}); v=sf(x.get("v")); c=sf(x.get("c"))
    sc=(4 if v>=1e10 else 0)+(4 if v>=3e10 else 0)+(4 if v>=1e11 else 0)+(3 if c>2 else 0)+(3 if c>5 else 0)
    return min(sc,15), (f"KR거래대금 {v/1e8:.1f}억 / KR등락 {c:.2f}%" if v else "KR 미상장/데이터 없음"), v

@dataclass
class Result:
    sym:str; price:float; score:float; action:str; stage:str; support:float; resistance:float; entry_low:float; entry_high:float; stop:float; target1:float; target2:float
    prob24:float; prob3d:float; prob7d:float; vol_ratio:float; buy_ratio:float; rsi:float; kr:float; cg:float; accumulation:float; smart:float; whale:float; squeeze:float; confidence:float; distribution:float; bubble:float; cg_text:str; liq:str; kr_text:str; warning:str; reason:str

def analyze(sym,kr):
    s=sym.upper().replace("USDT",""); k=klines(s); c=[x["c"] for x in k]; h=[x["h"] for x in k]; l=[x["l"] for x in k]; q=[x["qv"] for x in k]; b=[x["tbq"] for x in k]
    price=c[-1]; ma5=sma(c,5); ma20=sma(c,20); ma60=sma(c,60); mh=macd(c); rr=rsi(c); at=atr(h,l,c)
    vr=avg(q[-3:])/avg(q[-60:-15]) if avg(q[-60:-15]) else 1; br=avg(b[-3:])/avg(q[-3:]) if avg(q[-3:]) else 0.5
    cg=cg_snap(s); ks,kt,kv=kr_score(s,kr)
    chart=(5 if price>ma5 else 0)+(6 if price>ma20 else 0)+(4 if ma5>ma20 else 0)+(3 if price>ma60 else 0)+(2 if min(l[-30:])>=min(l[-60:-30])*0.98 else 0)
    volume=min(max((vr-1)*7,0),12)+(3 if br>0.60 else 2 if br>0.56 else 1 if br>0.52 else 0); volume=min(volume,15)
    momentum=(2 if 45<=rr<=68 else 0)+(2 if mh>0 else 0)+(1 if c[-1]>c[-4] else 0)
    chg24=pct(c[-1],c[-7]); risk=max(0,10-(3 if chg24>25 else 0)-(4 if chg24>45 else 0)-(3 if price<ma20 else 0))
    score=round(chart+volume+ks+cg["cg_score"]+momentum+risk,2)
    fund=cg["fund"]
    acc=clamp(cg["oi"]*2,0,25)+(18 if -0.08<=fund<=0.02 else 8 if fund<=0.05 else 2)+clamp((vr-1)*18,0,18)+(12 if br>=0.52 else 4)+ks*1.2+(10 if price>=ma20 else 3)+(8 if mh>0 else 0); acc=round(clamp(acc),1)
    dist=clamp(chg24*1.2,0,35)+clamp((vr-2)*12,0,25)+(20 if br<0.48 else 10 if br<0.52 else 0)+(15 if rr>75 else 8 if rr>68 else 0)+(10 if fund>0.05 else 0); dist=round(clamp(dist),1)
    bub=clamp(chg24*1.5,0,35)+(20 if rr>75 else 10 if rr>68 else 0)+(15 if fund>0.05 else 6 if fund>0.02 else 0)+clamp((vr-3)*10,0,20)+(10 if price>ma60*1.25 else 0); bub=round(clamp(bub),1)
    whale=round(clamp((vr-1)*25+(15 if br>0.56 else 0)+(10 if ks>=8 else 0)+(10 if cg["oi"]>=10 else 0)),1)
    squeeze=round(clamp(cg["oi"]*2+(25 if -0.08<=fund< -0.01 else 15 if fund<=0.02 else 3)+cg["liq_score"]*5+(10 if price>=ma20 else 0)),1)
    conf=round(clamp((18 if cg["oi_score"] else 0)+(14 if cg["fund_score"] else 0)+(10 if cg["taker_score"] else 0)+(8 if cg["liq_score"] else 0)+(10 if kv else 0)+(10 if price>=ma20 else 0)+(8 if vr>=1.2 else 0)+(8 if br>=0.52 else 0)+(7 if mh>0 else 0)+(7 if acc>dist else 0)),1)
    smart=round(clamp(acc*.45+conf*.25+squeeze*.2+whale*.1-bub*.15-dist*.15),1)
    base=35+acc*.3+squeeze*.2+conf*.15-bub*.2-dist*.15; p24=round(clamp(base,5,95),1); p3=round(clamp(base+(8 if acc>60 else 0),5,97),1); p7=round(clamp(base+(14 if acc>70 else 5),5,98),1)
    band=max((at/price if price else .03),.025); el=round(price*(1-band*.55),8); eh=round(price*(1+band*.15),8); st=round(price*(1-band*1.2),8); t1=round(price*(1+band*1.8),8); t2=round(price*(1+band*3.2),8)
    action="데이터 부족 — 관망" if conf<35 else "추격금지" if bub>=75 or dist>=75 else "대기" if price<ma20 else "분할매수/적극검토" if score>=85 and acc>=70 else "눌림 분할매수" if score>=70 and acc>=55 else "관망"
    stage="5단계 급등시작" if score>=92 and vr>=2 else "4단계 폭발직전" if acc>=80 else "3단계 수급증가" if acc>=65 else "2단계 매집관찰" if acc>=50 else "1단계 관찰"
    warn=[] 
    if bub>=70: warn.append("과열")
    if dist>=70: warn.append("분배")
    if conf<45: warn.append("신뢰도 낮음")
    if price<ma20: warn.append("MA20 아래")
    reason=[]
    if acc>=70: reason.append("매집 강함")
    if conf>=70: reason.append("신뢰도 양호")
    if ks>=8: reason.append("KR수급")
    if cg["cg_score"]>=18: reason.append("선물수급")
    if score<60: reason.append("점수 낮음")
    return Result(s+"USDT",round(price,8),score,action,stage,round(min(l[-20:]),8),round(max(h[-20:]),8),el,eh,st,t1,t2,p24,p3,p7,round(vr,2),round(br,3),round(rr,2),round(ks,2),round(cg["cg_score"],2),acc,smart,whale,squeeze,conf,dist,bub,f"OI {cg['oi']}% / Funding {cg['fund']}% / Taker {cg['taker']} / L/S {cg['ls']}",cg["liq"],kt," / ".join(warn) if warn else "특이위험 낮음"," / ".join(reason) if reason else "뚜렷한 강점 부족")

def scan(symbols):
    kr=kr_data(); out=[]
    for s in symbols:
        try: out.append(analyze(s,kr))
        except Exception as e: log(f"{s} error {e}"); log(traceback.format_exc())
        time.sleep(.08)
    return sorted(out,key=lambda r:(r.smart,r.score),reverse=True)
def full(r):
    return (f"🟢 <b>{r.sym}</b> {stars(r.score)}\n<b>A100 SCORE</b> {r.score}점 / {grade(r.score)}\nAI결론: <b>{r.action}</b>\n현재단계: <b>{r.stage}</b>\n핵심이유: {r.reason}\n\n"
            f"세력매집  {bar(r.accumulation)} {r.accumulation}%\n스마트머니 {bar(r.smart)} {r.smart}%\n고래대체  {bar(r.whale)} {r.whale}%\n숏스퀴즈  {bar(r.squeeze)} {r.squeeze}%\n신뢰도    {bar(r.confidence)} {r.confidence}%\n분배위험  {bar(r.distribution)} {r.distribution}%\n버블위험  {bar(r.bubble)} {r.bubble}%\n\n"
            f"가격: <code>{r.price}</code>\n지지/저항: <code>{r.support}</code> / <code>{r.resistance}</code>\n진입: <code>{r.entry_low}~{r.entry_high}</code>\n손절: <code>{r.stop}</code>\n목표: <code>{r.target1}</code> / <code>{r.target2}</code>\n확률: 24h {r.prob24}% | 3d {r.prob3d}% | 7d {r.prob7d}%\n\n"
            f"수급: KR {r.kr}/15 | CG {r.cg}/35 | Vol {r.vol_ratio}x | 매수비율 {r.buy_ratio}\nCG: {r.cg_text}\nKR: {r.kr_text}\n경고: {r.warning}\n")

def explosion_score(r):
    score = 0
    score += min(max((r.vol_ratio - 1) * 12, 0), 18)
    score += min(max(r.accumulation * 0.22, 0), 22)
    score += min(max(r.smart * 0.18, 0), 18)
    score += min(max(r.squeeze * 0.15, 0), 15)
    score += min(max(r.confidence * 0.12, 0), 12)
    score += 8 if r.action in ["분할매수/적극검토", "눌림 분할매수"] else 0
    score += 5 if r.bubble < 65 and r.distribution < 65 else -12
    return round(clamp(score), 1)

def quality_score(r):
    # 추천 품질: 단순 급등 가능성보다 신뢰도와 리스크를 더 반영
    q = r.smart * 0.30 + r.accumulation * 0.25 + r.confidence * 0.20 + explosion_score(r) * 0.20
    q -= r.bubble * 0.10
    q -= r.distribution * 0.10
    return round(clamp(q), 1)



def market_regime():
    # BTC 4H 기준 시장상태 자동판정
    try:
        k = klines("BTC")
        c = [x["c"] for x in k]
        price = c[-1]
        ma20 = sma(c, 20)
        ma60 = sma(c, 60)
        mh = macd(c)
        rr = rsi(c)
        if price > ma20 > ma60 and mh > 0:
            return "상승장", 0
        if price < ma20 and price < ma60:
            return "하락장", 12
        if price < ma20:
            return "약세횡보", 7
        if rr > 72:
            return "과열장", 8
        return "횡보장", 5
    except Exception as e:
        log(f"market_regime error {e}")
        return "중립", 5

def adaptive_thresholds():
    regime, add = market_regime()
    return {
        "regime": regime,
        "quality": 60 + add,
        "explosion": 55 + add,
        "confidence": 50 + max(0, add - 3),
        "accumulation": 55 + max(0, add - 4),
        "only_quality": 70 + add,
        "only_explosion": 65 + add,
        "only_confidence": 60 + max(0, add - 4),
        "only_accumulation": 65 + max(0, add - 5),
    }

def market_header():
    th = adaptive_thresholds()
    return (
        f"시장상태: <b>{th['regime']}</b>\n"
        f"Elite기준: 품질 {th['quality']}↑ / 폭발 {th['explosion']}↑ / 신뢰 {th['confidence']}↑ / 매집 {th['accumulation']}↑"
    )


def strict_action(r):
    q = quality_score(r)
    ex = explosion_score(r)
    if r.bubble >= 78 or r.distribution >= 78:
        return "🔴 위험"
    if q >= 82 and ex >= 75 and r.confidence >= 65 and r.accumulation >= 70:
        return "🔥 적극검토"
    if q >= 70 and ex >= 62 and r.confidence >= 55 and r.accumulation >= 60:
        return "🟢 분할매수"
    if q >= 58 and r.confidence >= 45 and r.accumulation >= 50:
        return "🟡 눌림대기"
    return "⚪ 관망"

def strict_pass(r):
    q = quality_score(r)
    ex = explosion_score(r)
    th = adaptive_thresholds()
    return (
        q >= th["quality"]
        and ex >= th["explosion"]
        and r.confidence >= th["confidence"]
        and r.accumulation >= th["accumulation"]
        and r.bubble < 75
        and r.distribution < 75
        and "관망" not in strict_action(r)
        and "위험" not in strict_action(r)
    )

def only_pass(r):
    q = quality_score(r)
    ex = explosion_score(r)
    th = adaptive_thresholds()
    return (
        q >= th["only_quality"]
        and ex >= th["only_explosion"]
        and r.confidence >= th["only_confidence"]
        and r.accumulation >= th["only_accumulation"]
        and r.smart >= 55
        and r.cg >= 10
        and r.bubble < 70
        and r.distribution < 70
        and ("분할매수" in strict_action(r) or "적극" in strict_action(r))
    )

def stage_visual(r):
    if r.accumulation >= 80:
        return "4단계 폭발직전\n■■■■■"
    if r.accumulation >= 65:
        return "3단계 잠금완료\n■■■■□"
    if r.accumulation >= 50:
        return "2단계 세력흡수\n■■■□□"
    return "1단계 초기관찰\n■■□□□"

def strict_reason(r):
    arr = []
    if r.accumulation >= 65: arr.append("매집 증가")
    if r.smart >= 55: arr.append("스마트머니 양호")
    if r.squeeze >= 55: arr.append("스퀴즈 가능")
    if r.confidence >= 60: arr.append("신뢰도 양호")
    if r.kr >= 8: arr.append("KR 수급")
    if r.cg >= 15: arr.append("선물수급")
    if r.vol_ratio >= 1.3: arr.append("거래량 증가")
    if r.bubble >= 70: arr.append("과열주의")
    if r.distribution >= 70: arr.append("분배주의")
    return " / ".join(arr) if arr else r.reason


def verdict_icon(r):
    ex = explosion_score(r)
    if ex >= 80 and r.confidence >= 45:
        return "🔥"
    if quality_score(r) >= 65:
        return "🟢"
    if r.bubble >= 70 or r.distribution >= 70:
        return "⚠️"
    return "🟡"



def bottom_score(r):
    # 바닥 매집 감지: 과열 낮고, 매집/스마트/신뢰가 살아있는 후보
    b = 0
    b += 25 if r.bubble < 35 else 18 if r.bubble < 50 else 8 if r.bubble < 65 else 0
    b += 20 if r.distribution < 35 else 12 if r.distribution < 55 else 0
    b += min(max(r.accumulation * 0.22, 0), 22)
    b += min(max(r.smart * 0.16, 0), 16)
    b += 10 if r.confidence >= 55 else 5 if r.confidence >= 45 else 0
    b += 7 if r.vol_ratio >= 1.0 else 0
    return round(clamp(b), 1)

def breakout_score(r):
    # 돌파 직전 점수: 저항 근접 + 거래량 + 매집 + 스퀴즈
    try:
        dist_to_res = (r.resistance - r.price) / r.price * 100 if r.price else 999
    except Exception:
        dist_to_res = 999
    s = 0
    s += 25 if 0 <= dist_to_res <= 3 else 18 if 3 < dist_to_res <= 7 else 8 if 7 < dist_to_res <= 12 else 0
    s += min(max((r.vol_ratio - 1) * 14, 0), 18)
    s += min(max(r.squeeze * 0.20, 0), 20)
    s += min(max(r.accumulation * 0.16, 0), 16)
    s += 10 if r.buy_ratio >= 0.52 else 0
    s -= 12 if r.bubble >= 70 or r.distribution >= 70 else 0
    return round(clamp(s), 1)

def whale_score(r):
    # 고래/세력 대체 점수
    w = 0
    w += min(max(r.whale * 0.35, 0), 35)
    w += min(max(r.smart * 0.25, 0), 25)
    w += min(max(r.accumulation * 0.20, 0), 20)
    w += 10 if r.kr >= 8 else 0
    w += 10 if r.vol_ratio >= 1.5 and r.buy_ratio >= 0.52 else 0
    return round(clamp(w), 1)

def tenx_score(r):
    # 10배 후보 점수: 저점 매집 + 스마트머니 + 과열 낮음 + 스퀴즈
    x = 0
    x += bottom_score(r) * 0.25
    x += whale_score(r) * 0.22
    x += breakout_score(r) * 0.18
    x += r.squeeze * 0.15
    x += r.confidence * 0.10
    x += 10 if r.bubble < 45 and r.distribution < 45 else 0
    x -= 20 if r.bubble >= 70 or r.distribution >= 70 else 0
    return round(clamp(x), 1)


def trend_power(r):
    # 4H 추세 강도: 과열 추격보다 눌림 후 회복을 선호
    p = 0
    p += 18 if r.price > r.entry_low else 5
    p += 16 if r.vol_ratio >= 1.2 else 8 if r.vol_ratio >= 0.9 else 0
    p += 16 if r.buy_ratio >= 0.52 else 6 if r.buy_ratio >= 0.49 else 0
    p += 15 if r.accumulation >= 60 else 8 if r.accumulation >= 48 else 0
    p += 12 if r.confidence >= 55 else 5
    p -= 15 if r.bubble >= 68 else 0
    p -= 12 if r.distribution >= 65 else 0
    return round(clamp(p), 1)

def chase_risk(r):
    # 고점추격 위험
    cr = 0
    cr += 30 if r.bubble >= 70 else 18 if r.bubble >= 55 else 5
    cr += 25 if r.distribution >= 70 else 15 if r.distribution >= 55 else 5
    cr += 18 if r.rsi >= 72 else 10 if r.rsi >= 66 else 0
    cr += 12 if r.vol_ratio >= 3.0 and r.buy_ratio < 0.52 else 0
    return round(clamp(cr), 1)

def real_signal_score(r):
    # V23 실전 신호: 24h 내 터질 확률 중심
    s = 0
    s += trend_power(r) * 0.18
    s += breakout_score(r) * 0.18
    s += timing_score(r) * 0.18
    s += whale_score(r) * 0.14
    s += r.squeeze * 0.14
    s += r.confidence * 0.12
    s += r.kr * 0.8
    s += r.cg * 0.35
    s -= chase_risk(r) * 0.20
    return v30_macro_adjust_score(r, round(clamp(s), 1))



def env_num(name, default=0.0):
    return safe_num(os.getenv(name, str(default)), default)

def v30_base_macro_engine():
    # 외부 API 과부하 방지를 위해 기본은 Environment 수동/반자동 입력 기반
    base_risk, note, fomc, cpi, war = macro_risk_score()

    ppi = env_num("PPI_DAYS", 99)
    pce = env_num("PCE_DAYS", 99)
    nfp = env_num("NFP_DAYS", 99)
    gdp = env_num("GDP_DAYS", 99)

    fg = env_num("FEAR_GREED", 50)          # 0~100
    dxy = env_num("DXY_TREND", 0)           # -100~100, +면 달러강세
    vix = env_num("VIX_LEVEL", 15)          # VIX 수치
    btc_dom = env_num("BTC_DOM_TREND", 0)   # +면 BTC 흡성
    etf = env_num("ETF_FLOW_M", 0)          # 백만달러 단위, +유입 -유출
    news = env_num("NEWS_RISK", 0)          # 지정학/규제뉴스 0~100

    risk = base_risk
    event_msgs = []

    def add_event(days, name, d1, d3):
        nonlocal risk
        if days <= 1:
            risk += d1
            event_msgs.append(f"{name} D-{int(days)} 고위험")
        elif days <= 3:
            risk += d3
            event_msgs.append(f"{name} D-{int(days)} 주의")

    add_event(fomc, "FOMC", 18, 10)
    add_event(cpi, "CPI", 15, 8)
    add_event(ppi, "PPI", 10, 5)
    add_event(pce, "PCE", 12, 6)
    add_event(nfp, "NFP", 12, 6)
    add_event(gdp, "GDP", 8, 4)

    risk += min(max(war, 0), 25)
    risk += min(max(news * 0.35, 0), 25)

    if fg >= 80:
        risk += 12
        event_msgs.append("Fear&Greed 과열")
    elif fg <= 20:
        risk += 8
        event_msgs.append("Fear&Greed 공포")

    if dxy >= 30:
        risk += 12
        event_msgs.append("DXY 강세")
    elif dxy <= -30:
        risk -= 5
        event_msgs.append("DXY 약세")

    if vix >= 28:
        risk += 18
        event_msgs.append("VIX 급등")
    elif vix >= 22:
        risk += 10
        event_msgs.append("VIX 상승")

    if btc_dom >= 25:
        risk += 8
        event_msgs.append("BTC 도미넌스 상승: 알트 주의")
    elif btc_dom <= -25:
        risk -= 4
        event_msgs.append("BTC 도미넌스 하락: 알트 우호")

    if etf <= -300:
        risk += 12
        event_msgs.append("ETF 대량 유출")
    elif etf >= 300:
        risk -= 8
        event_msgs.append("ETF 대량 유입")

    risk = round(max(0, min(100, risk)), 1)

    if risk >= 75:
        mode = "🔴 리스크오프"
        guard = 14
    elif risk >= 60:
        mode = "🟠 방어모드"
        guard = 9
    elif risk >= 45:
        mode = "🟡 보수모드"
        guard = 5
    else:
        mode = "🟢 일반모드"
        guard = 0

    # 알트 감점/추천 강화 가중치
    alt_penalty = 0
    if dxy >= 30 or btc_dom >= 25 or vix >= 22 or risk >= 60:
        alt_penalty += 6
    if war >= 50 or news >= 60:
        alt_penalty += 6

    return {
        "risk": risk,
        "mode": mode,
        "guard": guard,
        "alt_penalty": alt_penalty,
        "note": note,
        "events": event_msgs,
        "fomc": fomc, "cpi": cpi, "ppi": ppi, "pce": pce, "nfp": nfp, "gdp": gdp,
        "fg": fg, "dxy": dxy, "vix": vix, "btc_dom": btc_dom, "etf": etf, "war": war, "news": news,
    }

def macro_guard_add():
    return v30_base_macro_engine()["guard"]

def v30_base_macro_report():
    m = v30_base_macro_engine()
    ev = " / ".join(m["events"]) if m["events"] else "특이 이벤트 없음"
    return (
        f"🌎 <b>A100 v30 매크로 엔진</b>\n"
        f"모드: <b>{m['mode']}</b>\n"
        f"종합위험: <b>{m['risk']}%</b> | 추천기준 +{m['guard']}점 | 알트감점 {m['alt_penalty']}점\n\n"
        f"일정: FOMC D-{int(m['fomc']) if m['fomc'] < 90 else '?'} / CPI D-{int(m['cpi']) if m['cpi'] < 90 else '?'} / PPI D-{int(m['ppi']) if m['ppi'] < 90 else '?'} / PCE D-{int(m['pce']) if m['pce'] < 90 else '?'} / NFP D-{int(m['nfp']) if m['nfp'] < 90 else '?'}\n"
        f"시장: FearGreed {m['fg']} / DXY {m['dxy']} / VIX {m['vix']} / BTC.D {m['btc_dom']} / ETF {m['etf']}M\n"
        f"지정학: 전쟁 {m['war']}% / 뉴스위험 {m['news']}%\n"
        f"이벤트: {ev}\n"
        f"메모: {m['note']}\n\n"
        f"AI판정: {'알트 고배율 금지 / BTC 우선 / 손절 짧게' if m['risk'] >= 60 else '일반 기준, 단 추격매수 금지'}"
    )

def v30_macro_adjust_score(r, score):
    m = v30_base_macro_engine()
    s = score
    # BTC/ETH는 리스크오프 때 알트보다 덜 감점
    major = r.sym.startswith(("BTC", "ETH"))
    if not major:
        s -= m["alt_penalty"]
    if m["risk"] >= 75:
        s -= 10 if not major else 4
    elif m["risk"] >= 60:
        s -= 6 if not major else 2
    if m["etf"] >= 300 and major:
        s += 4
    return round(clamp(s), 1)

def v30_real_thresholds():
    regime, add = market_regime()
    guard = macro_guard_add()
    if regime == "상승장":
        base = {"regime": regime, "real": 46, "timing": 38, "breakout": 28, "accumulation": 43, "confidence": 43, "chase": 65}
    elif regime == "횡보장":
        base = {"regime": regime, "real": 46, "timing": 40, "breakout": 30, "accumulation": 43, "confidence": 43, "chase": 65}
    elif regime == "약세횡보":
        base = {"regime": regime, "real": 50, "timing": 42, "breakout": 33, "accumulation": 46, "confidence": 46, "chase": 62}
    elif regime == "하락장":
        base = {"regime": regime, "real": 56, "timing": 48, "breakout": 38, "accumulation": 50, "confidence": 50, "chase": 58}
    elif regime == "과열장":
        base = {"regime": regime, "real": 54, "timing": 46, "breakout": 36, "accumulation": 48, "confidence": 50, "chase": 55}
    else:
        base = {"regime": regime, "real": 48, "timing": 40, "breakout": 30, "accumulation": 44, "confidence": 44, "chase": 63}
    base["real"] += guard
    base["timing"] += max(0, guard - 2)
    base["confidence"] += max(0, guard - 4)
    base["chase"] -= min(10, guard)
    return base


def v30_header():
    th = v30_real_thresholds()
    return (
        f"시장상태: <b>{th['regime']}</b>\n"
        f"실전기준: 실전 {th['real']}↑ / 타이밍 {th['timing']}↑ / 돌파 {th['breakout']}↑ / 매집 {th['accumulation']}↑ / 신뢰 {th['confidence']}↑\n매크로가드: +{macro_guard_add()}점 / {v30_macro_engine()['mode']}"
    )

def v30_best_fallback(res, n=3):
    return sorted(
        res,
        key=lambda r: (real_signal_score(r), timing_score(r), breakout_score(r), whale_score(r), -chase_risk(r)),
        reverse=True
    )[:n]

def format_fallback(r, rank=1):
    return (
        f"🟡 <b>{rank}. {r.sym}</b>\n"
        f"실전 {real_signal_score(r)}% | 타이밍 {timing_score(r)}% | 돌파 {breakout_score(r)}% | 추격위험 {chase_risk(r)}%\n"
        f"판정: <b>{v30_decision(r)}</b>\n"
        f"진입관찰 <code>{r.entry_low}~{r.entry_high}</code> / 손절 <code>{r.stop}</code>\n"
        f"이유: {v30_reason(r)}\n"
    )


def real_pass(r):
    th = v30_real_thresholds()
    rs = real_signal_score(r)
    return (
        rs >= th["real"]
        and timing_score(r) >= th["timing"]
        and r.accumulation >= th["accumulation"]
        and r.confidence >= th["confidence"]
        and chase_risk(r) < th["chase"]
        and r.distribution < 72
        and r.bubble < 75
    )


def god_v30_pass(r):
    th = v30_real_thresholds()
    return (
        real_signal_score(r) >= max(th["real"] + 3, 48)
        and timing_score(r) >= max(th["timing"] + 2, 40)
        and breakout_score(r) >= th["breakout"]
        and r.accumulation >= max(th["accumulation"], 45)
        and r.confidence >= max(th["confidence"], 45)
        and chase_risk(r) < min(th["chase"], 62)
        and r.bubble < 72
        and r.distribution < 72
    )


def v30_decision(r):
    rs = real_signal_score(r)
    if chase_risk(r) >= 70 or r.distribution >= 75:
        return "🔴 추격금지"
    if rs >= 70 and timing_score(r) >= 60:
        return "🔥 24H 폭발후보"
    if rs >= 58:
        return "🟢 실전 관심"
    if rs >= 48:
        return "🟡 관찰"
    return "⚪ 대기"

def v30_reason(r):
    arr = []
    if real_signal_score(r) >= 55: arr.append("실전신호 양호")
    if trend_power(r) >= 50: arr.append("추세회복")
    if breakout_score(r) >= 45: arr.append("저항 돌파권")
    if timing_score(r) >= 50: arr.append("타이밍 양호")
    if whale_score(r) >= 45: arr.append("고래/세력 흔적")
    if r.squeeze >= 45: arr.append("스퀴즈 압력")
    if r.kr >= 6: arr.append("KR수급")
    if r.cg >= 12: arr.append("선물수급")
    if chase_risk(r) >= 55: arr.append("추격주의")
    return " / ".join(arr) if arr else "신호 약함"

def format_real(r, rank=1):
    return (
        f"⚡ <b>{rank}. {r.sym}</b> {stars(real_signal_score(r))}\n"
        f"실전신호 {real_signal_score(r)}% | GOD {god_score(r)}% | 10X {tenx_score(r)}%\n"
        f"24H타이밍 {timing_score(r)}% | 추세 {trend_power(r)}% | 추격위험 {chase_risk(r)}%\n"
        f"돌파 {breakout_score(r)}% | 고래 {whale_score(r)}% | 스퀴즈 {r.squeeze}% | 승률 {win_rate_estimate(r)}%\n"
        f"AI판정: <b>{v30_decision(r)}</b>\n"
        f"진입 <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절 <code>{r.stop}</code> | 목표 <code>{r.target1}</code> / <code>{r.target2}</code>\n"
        f"이유: {v30_reason(r)}\n"
        f"리스크: 버블 {r.bubble}% / 분배 {r.distribution}%\n"
    )


def god_score(r):
    # 최종 GOD 점수: 폭발·타이밍·10배후보·승률 종합
    g = (
        real_signal_score(r) * 0.26
        + explosion_score(r) * 0.16
        + timing_score(r) * 0.16
        + quality_score(r) * 0.14
        + tenx_score(r) * 0.12
        + whale_score(r) * 0.08
        + win_rate_estimate(r) * 0.08
    )
    g -= 15 if chase_risk(r) >= 70 or r.distribution >= 70 else 0
    return round(clamp(g), 1)

def god_pass(r):
    return (
        god_score(r) >= 62
        and r.confidence >= 48
        and r.accumulation >= 50
        and r.bubble < 72
        and r.distribution < 72
    )

def god_reason(r):
    arr = []
    if bottom_score(r) >= 60: arr.append("바닥매집")
    if breakout_score(r) >= 55: arr.append("돌파직전")
    if whale_score(r) >= 55: arr.append("고래/세력 수급")
    if r.squeeze >= 50: arr.append("숏스퀴즈 가능")
    if r.vol_ratio >= 1.3: arr.append("거래량 증가")
    if r.cg >= 15: arr.append("선물수급")
    if r.kr >= 8: arr.append("KR수급")
    if r.bubble >= 65: arr.append("과열주의")
    return " / ".join(arr) if arr else "조건 약함"

def format_god(r, rank=1):
    return (
        f"🔥 <b>{rank}. {r.sym}</b> {stars(god_score(r))}\n"
        f"실전 {real_signal_score(r)}% | GOD {god_score(r)}% | 10X {tenx_score(r)}% | 타이밍 {timing_score(r)}% | 승률 {win_rate_estimate(r)}% | RR {rr_score(r)}\n"
        f"바닥 {bottom_score(r)}% | 돌파 {breakout_score(r)}% | 고래 {whale_score(r)}% | 스퀴즈 {r.squeeze}%\n"
        f"AI신호: <b>{entry_signal(r)}</b>\n"
        f"진입 <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절 <code>{r.stop}</code> | 목표 <code>{r.target1}</code> / <code>{r.target2}</code>\n"
        f"이유: {god_reason(r)}\n"
        f"리스크: 버블 {r.bubble}% / 분배 {r.distribution}%\n"
    )


def timing_score(r):
    # 지금 진입 타이밍 점수: 좋은 코인보다 "지금 자리"를 더 중시
    t = 0
    t += min(max((r.vol_ratio - 1.0) * 18, 0), 22)
    t += 18 if r.accumulation >= 60 else (10 if r.accumulation >= 50 else 3)
    t += 15 if r.smart >= 50 else (8 if r.smart >= 40 else 2)
    t += 12 if r.squeeze >= 45 else (6 if r.squeeze >= 30 else 1)
    t += 12 if r.confidence >= 55 else (6 if r.confidence >= 45 else 0)
    t += 8 if r.buy_ratio >= 0.52 else 0
    # 과열/분배는 타이밍 감점
    t -= 18 if r.bubble >= 70 else (8 if r.bubble >= 55 else 0)
    t -= 18 if r.distribution >= 70 else (8 if r.distribution >= 55 else 0)
    return round(clamp(t), 1)

def rr_score(r):
    try:
        risk = abs(r.entry_high - r.stop)
        reward = abs(r.target1 - r.entry_high)
        rr = reward / risk if risk else 0
    except Exception:
        rr = 0
    return round(rr, 2)

def win_rate_estimate(r):
    wr = 35
    wr += quality_score(r) * 0.22
    wr += timing_score(r) * 0.20
    wr += r.confidence * 0.15
    wr += 5 if rr_score(r) >= 1.5 else -5
    wr -= 10 if r.bubble >= 70 or r.distribution >= 70 else 0
    return round(clamp(wr, 5, 90), 1)

def entry_signal(r):
    ts = timing_score(r)
    q = quality_score(r)
    if r.bubble >= 75 or r.distribution >= 75:
        return "🔴 진입금지"
    if ts >= 72 and q >= 65 and r.confidence >= 55:
        return "🚨 지금 진입 후보"
    if ts >= 58 and q >= 55:
        return "🟢 눌림 진입 후보"
    if r.accumulation >= 50 and r.smart >= 35:
        return "🟡 관심 유지"
    return "⚪ 대기"

def timing_reason(r):
    arr = []
    if r.vol_ratio >= 1.3: arr.append("거래량 증가")
    if r.accumulation >= 60: arr.append("매집 양호")
    if r.smart >= 50: arr.append("스마트머니")
    if r.squeeze >= 45: arr.append("스퀴즈 가능")
    if r.buy_ratio >= 0.52: arr.append("매수비율 우세")
    if r.confidence >= 55: arr.append("신뢰도 양호")
    if r.bubble >= 70: arr.append("과열주의")
    if r.distribution >= 70: arr.append("분배주의")
    return " / ".join(arr) if arr else "아직 타이밍 약함"

def timing_pass(r):
    return (
        timing_score(r) >= 55
        and quality_score(r) >= 52
        and r.confidence >= 45
        and r.accumulation >= 50
        and r.bubble < 75
        and r.distribution < 75
    )


def format_elite(r, rank=1):
    ex = explosion_score(r)
    q = quality_score(r)
    sa = strict_action(r)
    return (
        f"{verdict_icon(r)} <b>{rank}. {r.sym}</b> {stars(q)}\n"
        f"<b>추천품질</b> {q}% | <b>폭발확률</b> {ex}%\n"
        f"매집 {r.accumulation}% | 스마트 {r.smart}% | 스퀴즈 {r.squeeze}% | 신뢰 {r.confidence}%\n"
        f"AI판정: <b>{sa}</b>\n"
        f"진입타이밍: <b>{entry_signal(r)}</b> | 타이밍 {timing_score(r)}% | 승률 {win_rate_estimate(r)}% | RR {rr_score(r)}\n"
        f"GOD {god_score(r)}% | 10X {tenx_score(r)}% | 바닥 {bottom_score(r)}% | 돌파 {breakout_score(r)}% | 고래 {whale_score(r)}%\n"
        f"단계: {stage_visual(r)}\n"
        f"진입 <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절 <code>{r.stop}</code> | TP1 <code>{r.target1}</code> | TP2 <code>{r.target2}</code>\n"
        f"리스크: 버블 {r.bubble}% / 분배 {r.distribution}%\n"
        f"이유: {strict_reason(r)}\n"
        f"타이밍이유: {timing_reason(r)}\n"
    )

def elite_filter(res):
    # 너무 위험한 과열/분배 후보 제외, 데이터 신뢰도 최소 요구
    return [r for r in res if strict_pass(r)]

def elite_sort(res):
    return sorted(elite_filter(res), key=lambda r: (quality_score(r), explosion_score(r), r.smart, r.score), reverse=True)


def ranktxt(res,n=10):
    ranked = elite_sort(res) if res else []
    lines = ["⚡ <b>A100 v30 Adaptive Signal Rank</b>", market_header(), "추천품질·폭발확률 기준으로 재정렬\n"]
    for i, r in enumerate(ranked[:n], 1):
        lines.append(format_elite(r, i))
    return "\n".join(lines) if ranked else "A100 후보 없음"

def report(symbols,n=10):
    res=scan(symbols)
    return "A100 결과 없음" if not res else "🔥 <b>A100 v30 Korean News Meta AI</b>\n폭발확률·추천품질 중심 분석\n\n"+"\n━━━━━━━━━━━━\n".join(full(r) for r in elite_sort(res)[:n])

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE): await update.message.reply_text("A100 v30 시작\n/check\n/scan ARKM,SYN,SENT\n/macro\n/live\n/news\n/final\n/mode\n/events\n/macrohelp\n/cgstatus\n/rank\n/hot\n/sniper\n/elite\n/only\n/auto\n/god\n/real\n/scalp\n/tenx\n/breakout\n/bottom\n/timing\n/now\n/win ARKM,SYN\n/smart\n/danger\n/watch\n/risk ARKM,SYN\n/kr\n/cgtest BTC\n/myid")
async def myid(update,context): await update.message.reply_text(f"TELEGRAM_CHAT_ID = {update.effective_chat.id}")
async def check(update,context): await update.message.reply_text("A100 분석 중..."); await update.message.reply_text(report(DEFAULT_SYMBOLS,10),parse_mode="HTML")
async def scan_cmd(update,context):
    raw=" ".join(context.args).strip()
    if not raw: await update.message.reply_text("예: /scan ARKM,SYN,SENT"); return
    syms=[x.strip().upper() for x in raw.replace(" ","").split(",") if x.strip()]
    await update.message.reply_text("A100 분석 중..."); await update.message.reply_text(report(syms,10),parse_mode="HTML")
async def rank_cmd(update,context): await update.message.reply_text("A100 랭킹 스캔 중..."); await update.message.reply_text(ranktxt(scan(top_usdt(TOP_SCAN_LIMIT)),15),parse_mode="HTML")
async def hot_cmd(update,context):
    await update.message.reply_text("A100 HOT 후보 스캔 중..."); res=scan(top_usdt(TOP_SCAN_LIMIT)); hot=[r for r in elite_sort(res) if explosion_score(r)>=45 or r.accumulation>=55]
    await update.message.reply_text(ranktxt(hot,10) if hot else "HOT 후보 없음",parse_mode="HTML")

async def sniper_cmd(update,context):
    await update.message.reply_text("🎯 A100 v30 스나이퍼 단일 후보 스캔 중...")
    res = elite_sort(scan(top_usdt(TOP_SCAN_LIMIT)))
    if not res:
        await update.message.reply_text("🎯 오늘은 스나이퍼 후보 없음\n\n기준 미달이면 억지 추천하지 않습니다.\n무리하게 진입하지 않는 것이 더 좋습니다.")
        return
    r = res[0]
    if not strict_pass(r):
        await update.message.reply_text("🎯 오늘은 스나이퍼 후보 없음\n\n추천품질/폭발확률/신뢰도/매집 조건 미달입니다.")
        return
    ex = explosion_score(r)
    q = quality_score(r)
    text = (
        "🎯 <b>A100 v30 SNIPER PICK</b>\n\n"
        f"<b>{r.sym}</b> {stars(q)}\n"
        f"추천품질: <b>{q}%</b>\n"
        f"폭발확률: <b>{ex}%</b>\n"
        f"AI판정: <b>{strict_action(r)}</b>\n\n"
        f"단계:\n{stage_visual(r)}\n\n"
        f"매집 {bar(r.accumulation)} {r.accumulation}%\n"
        f"스마트 {bar(r.smart)} {r.smart}%\n"
        f"스퀴즈 {bar(r.squeeze)} {r.squeeze}%\n"
        f"신뢰도 {bar(r.confidence)} {r.confidence}%\n\n"
        f"진입: <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절: <code>{r.stop}</code>\n"
        f"목표: <code>{r.target1}</code> / <code>{r.target2}</code>\n"
        f"이유: {strict_reason(r)}\n"
        f"타이밍이유: {timing_reason(r)}\n"
        f"경고: {r.warning}"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def elite_cmd(update,context):
    await update.message.reply_text("🏆 A100 v30 Elite Pick TOP5 스캔 중...")
    res = elite_sort(scan(top_usdt(TOP_SCAN_LIMIT)))
    if not res:
        await update.message.reply_text("🏆 A100 ELITE\n\n오늘은 Elite 후보가 없습니다.\n무리한 진입보다 기다리는 것이 유리합니다.")
        return
    lines = ["🏆 <b>A100 v30 ELITE PICK TOP5</b>", market_header(), ""]
    for i, r in enumerate(res[:5], 1):
        lines.append(format_elite(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def only_cmd(update,context):
    await update.message.reply_text("🔥 A100 오늘 단 하나 후보 스캔 중...")
    res = elite_sort(scan(top_usdt(TOP_SCAN_LIMIT)))
    cand = [r for r in res if only_pass(r)]
    if not cand:
        await update.message.reply_text(
            "🔥 오늘 단 하나 후보 없음\n\n"
            "V20 적응형 기준 미달입니다.\n"
            "조건: 추천품질 70↑ / 폭발확률 65↑ / 신뢰도 60↑ / 매집 65↑ / 과열·분배 낮음"
        )
        return
    r = cand[0]
    q = quality_score(r)
    ex = explosion_score(r)
    text = (
        "🔥 <b>오늘 단 하나</b>\n\n"
        f"<b>{r.sym}</b> {stars(q)}\n\n"
        f"폭발확률 <b>{ex}%</b>\n"
        f"신뢰도 <b>{r.confidence}%</b>\n"
        f"추천품질 <b>{q}%</b>\n"
        f"진입타이밍 <b>{timing_score(r)}%</b>\n"
        f"예상승률 <b>{win_rate_estimate(r)}%</b> / RR <b>{rr_score(r)}</b>\n"
        f"AI판정 <b>{entry_signal(r)}</b>\n\n"
        f"예상수익\n"
        f"TP1: <code>{r.target1}</code>\n"
        f"TP2: <code>{r.target2}</code>\n\n"
        f"진입: <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절: <code>{r.stop}</code>\n\n"
        f"추천이유\n{strict_reason(r)}\n"
        f"CG: {r.cg_text}\n"
        f"KR: {r.kr_text}"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def risk_cmd(update,context):
    raw=" ".join(context.args).strip(); syms=[x.strip().upper() for x in raw.replace(" ","").split(",") if x.strip()] if raw else DEFAULT_SYMBOLS
    res=sorted(scan(syms),key=lambda r:r.bubble+r.distribution-r.confidence,reverse=True); lines=["⚠ <b>A100 위험도 TOP</b>\n"]+[f"{i}. <b>{r.sym}</b> | 버블 {r.bubble}% | 분배 {r.distribution}% | 신뢰 {r.confidence}% | {r.action}" for i,r in enumerate(res[:10],1)]
    await update.message.reply_text("\n".join(lines),parse_mode="HTML")
async def kr_cmd(update,context):
    k=kr_data(); arr=sorted([(s,x.get("v",0),x.get("c",0)) for s,x in k.items()],key=lambda x:x[1],reverse=True); lines=["🇰🇷 <b>업비트+빗썸 KRW 거래대금 상위</b>\n"]+[f"{i}. <b>{s}</b> | {v/1e8:.1f}억 | {c:.2f}%" for i,(s,v,c) in enumerate(arr[:20],1)]
    await update.message.reply_text("\n".join(lines),parse_mode="HTML")
async def cgtest_cmd(update,context):
    sym=context.args[0].upper() if context.args else "BTC"; c=cg_snap(sym)
    await update.message.reply_text(f"🧪 <b>CoinGlass {sym}</b>\nOI {c['oi']}% / Funding {c['fund']}%\nTaker {c['taker']} / L/S {c['ls']}\n청산 {c['liq']}\nCG Score {round(c['cg_score'],2)}/35",parse_mode="HTML")
def send(text):
    if not BOT_TOKEN or not CHAT_ID: log("TOKEN/CHAT_ID missing"); return
    try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",json={"chat_id":CHAT_ID,"text":text,"parse_mode":"HTML"},timeout=15)
    except Exception as e: log(f"telegram {e}")
def morning(): send("🌅 <b>A100 v30 오전 5시 Elite 리포트</b>\n\n"+report(DEFAULT_SYMBOLS,10))
def alert():
    hit=[r for r in scan(DEFAULT_SYMBOLS) if strict_pass(r) and (r.score>=SCORE_ALERT or r.accumulation>=80 or r.smart>=75 or r.squeeze>=75 or timing_score(r)>=72 or god_score(r)>=70 or real_signal_score(r)>=70)]
    if hit: send("🚨 <b>A100 v30 조건 감지</b>\n\n"+ranktxt(hit,5))



async def auto_cmd(update,context):
    await update.message.reply_text("🤖 A100 v30 자동판정 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if real_pass(r)]
    cand = sorted(cand, key=lambda r: (real_signal_score(r), timing_score(r), breakout_score(r)), reverse=True)
    lines = ["🤖 <b>A100 v30 AUTO THRESHOLD</b>", v30_header(), ""]
    if cand:
        lines.append("✅ 실전 후보")
        for i, r in enumerate(cand[:5], 1):
            lines.append(format_real(r, i))
    else:
        lines.append("⚪ 기준 통과 후보 없음\n관찰 TOP3")
        for i, r in enumerate(v30_best_fallback(res, 3), 1):
            lines.append(format_fallback(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def god_cmd(update,context):
    await update.message.reply_text("🔥 A100 v30 Auto GOD 실전 단일 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if god_v30_pass(r)]
    cand = sorted(cand, key=lambda r: (real_signal_score(r), god_score(r), timing_score(r), breakout_score(r)), reverse=True)
    if not cand:
        fb = v30_best_fallback(res, 3)
        lines = ["🔥 <b>GOD 실전 후보 없음</b>", v30_header(), "기준 미달이라 매수 추천은 하지 않습니다.\n현재 가장 나은 관찰 후보 TOP3:\n"]
        for i, r in enumerate(fb, 1):
            lines.append(format_fallback(r, i))
        await update.message.reply_text("\n".join(lines), parse_mode="HTML")
        return
    r = cand[0]
    text = (
        "🔥 <b>A100 v30 GOD PICK</b>\n"
        "24시간 내 실전 신호 단일 후보\n\n"
        + v30_header()
        + "\n\n"
        + format_real(r, 1)
        + f"\nCG: {r.cg_text}\nKR: {r.kr_text}"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def real_cmd(update,context):
    await update.message.reply_text("⚡ A100 v30 Auto 실전신호 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if real_pass(r)]
    cand = sorted(cand, key=lambda r: (real_signal_score(r), timing_score(r), breakout_score(r), whale_score(r)), reverse=True)
    if not cand:
        fb = v30_best_fallback(res, 3)
        lines = ["⚡ <b>실전신호 후보 없음</b>", v30_header(), "현재는 기다리는 구간입니다.\n그래도 관찰할 TOP3:\n"]
        for i, r in enumerate(fb, 1):
            lines.append(format_fallback(r, i))
        await update.message.reply_text("\n".join(lines), parse_mode="HTML")
        return
    lines = ["⚡ <b>A100 v30 REAL SIGNAL</b>", v30_header(), "24시간 내 터질 가능성 중심\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_real(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def scalp_cmd(update,context):
    await update.message.reply_text("⚔️ A100 단타 스캘핑 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [
        r for r in res
        if timing_score(r) >= 55 and r.vol_ratio >= 1.1 and r.buy_ratio >= 0.50 and chase_risk(r) < 65
    ]
    cand = sorted(cand, key=lambda r: (timing_score(r), real_signal_score(r), r.vol_ratio), reverse=True)
    if not cand:
        await update.message.reply_text("⚔️ 단타 후보 없음")
        return
    lines = ["⚔️ <b>A100 SCALP SIGNAL</b>", "단기 타이밍 중심. 손절 필수.\n"]
    for i, r in enumerate(cand[:8], 1):
        lines.append(format_real(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def timing_cmd(update,context):
    await update.message.reply_text("⏱ A100 v30 진입 타이밍 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if timing_pass(r)]
    cand = sorted(cand, key=lambda r: (timing_score(r), quality_score(r), win_rate_estimate(r)), reverse=True)
    if not cand:
        await update.message.reply_text("⏱ 지금 진입 타이밍 후보 없음\n\n기준 미달이면 기다리는 것이 유리합니다.")
        return
    lines = ["⏱ <b>A100 v30 TIMING AI</b>", market_header(), "지금 자리 기준 랭킹\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_elite(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def now_cmd(update,context):
    await update.message.reply_text("🚨 A100 지금 진입 후보 단일 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if timing_score(r) >= 65 and quality_score(r) >= 55 and god_score(r) >= 55 and r.confidence >= 50 and r.bubble < 70 and r.distribution < 70]
    cand = sorted(cand, key=lambda r: (timing_score(r), god_score(r), win_rate_estimate(r), quality_score(r)), reverse=True)
    if not cand:
        await update.message.reply_text("🚨 지금 진입 후보 없음\n\n기다리는 구간입니다.")
        return
    r = cand[0]
    text = (
        "🚨 <b>A100 v30 NOW ENTRY</b>\n\n"
        f"<b>{r.sym}</b> {stars(quality_score(r))}\n"
        f"진입타이밍: <b>{timing_score(r)}%</b>\n"
        f"추천품질: <b>{quality_score(r)}%</b>\n"
        f"예상승률: <b>{win_rate_estimate(r)}%</b>\n"
        f"RR: <b>{rr_score(r)}</b>\n"
        f"GOD: <b>{god_score(r)}%</b> | 10X: <b>{tenx_score(r)}%</b>\n"
        f"AI신호: <b>{entry_signal(r)}</b>\n\n"
        f"진입: <code>{r.entry_low}~{r.entry_high}</code>\n"
        f"손절: <code>{r.stop}</code>\n"
        f"목표: <code>{r.target1}</code> / <code>{r.target2}</code>\n\n"
        f"이유: {timing_reason(r)}\n"
        f"주의: {r.warning}"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def win_cmd(update,context):
    raw = " ".join(context.args).strip()
    syms = [x.strip().upper() for x in raw.replace(" ","").split(",") if x.strip()] if raw else top_usdt(TOP_SCAN_LIMIT)
    await update.message.reply_text("📊 A100 예상승률 계산 중...")
    res = scan(syms)
    res = sorted(res, key=lambda r: (win_rate_estimate(r), rr_score(r), quality_score(r)), reverse=True)
    lines = ["📊 <b>A100 v30 예상승률 TOP</b>\n"]
    for i, r in enumerate(res[:10], 1):
        lines.append(
            f"{i}. <b>{r.sym}</b>\n"
            f"승률 {win_rate_estimate(r)}% | RR {rr_score(r)} | 타이밍 {timing_score(r)}% | 품질 {quality_score(r)}%\n"
            f"신호: {entry_signal(r)}\n"
        )
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def smart_cmd(update,context):
    await update.message.reply_text("🧠 A100 스마트머니 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if r.smart >= 45 and r.accumulation >= 50 and r.distribution < 75]
    cand = sorted(cand, key=lambda r: (r.smart, r.accumulation, r.confidence), reverse=True)
    if not cand:
        await update.message.reply_text("🧠 스마트머니 후보 없음")
        return
    lines = ["🧠 <b>A100 SMART MONEY</b>"]
    try:
        lines.append(market_header())
    except Exception:
        pass
    lines.append("")
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_elite(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def danger_cmd(update,context):
    await update.message.reply_text("⚠️ A100 위험 후보 스캔 중...")
    raw = " ".join(context.args).strip()
    syms = [x.strip().upper() for x in raw.replace(" ","").split(",") if x.strip()] if raw else top_usdt(TOP_SCAN_LIMIT)
    res = scan(syms)
    bad = sorted(res, key=lambda r: (r.bubble + r.distribution - r.confidence), reverse=True)
    lines = ["⚠️ <b>A100 DANGER LIST</b>", "분배·과열·신뢰도 저하 후보\n"]
    for i, r in enumerate(bad[:10], 1):
        lines.append(
            f"{i}. <b>{r.sym}</b>\n"
            f"버블 {r.bubble}% | 분배 {r.distribution}% | 신뢰 {r.confidence}%\n"
            f"판정: <b>{strict_action(r)}</b>\n"
            f"경고: {r.warning}\n"
        )
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def watch_cmd(update,context):
    await update.message.reply_text("👀 A100 관심 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    watch = []
    for r in res:
        if not strict_pass(r) and r.accumulation >= 45 and r.smart >= 35 and r.bubble < 75:
            watch.append(r)
    watch = sorted(watch, key=lambda r: (r.accumulation, r.smart, r.confidence), reverse=True)
    if not watch:
        await update.message.reply_text("👀 관심 후보 없음")
        return
    lines = ["👀 <b>A100 WATCH LIST</b>", "아직 진입은 아니지만 관찰할 후보\n"]
    for i, r in enumerate(watch[:10], 1):
        lines.append(format_elite(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")



async def tenx_cmd(update,context):
    await update.message.reply_text("💎 A100 v30 10X 잠재 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if tenx_score(r) >= 48 and r.bubble < 70 and r.distribution < 70]
    cand = sorted(cand, key=lambda r: (tenx_score(r), bottom_score(r), whale_score(r)), reverse=True)
    if not cand:
        await update.message.reply_text("💎 10X 잠재 후보 없음")
        return
    lines = ["💎 <b>A100 v30 10X WATCH</b>", "초고위험 장기 잠재 후보입니다. 단타 매수신호가 아닙니다.\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def breakout_cmd(update,context):
    await update.message.reply_text("🚀 A100 v30 돌파직전 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if breakout_score(r) >= 45 and r.bubble < 75 and r.distribution < 75]
    cand = sorted(cand, key=lambda r: (breakout_score(r), timing_score(r), r.squeeze), reverse=True)
    if not cand:
        await update.message.reply_text("🚀 돌파직전 후보 없음")
        return
    lines = ["🚀 <b>A100 v30 BREAKOUT WATCH</b>", "저항 근접·거래량·스퀴즈 기준\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def bottom_cmd(update,context):
    await update.message.reply_text("🧱 A100 v30 바닥매집 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if bottom_score(r) >= 55 and r.accumulation >= 45 and r.bubble < 65]
    cand = sorted(cand, key=lambda r: (bottom_score(r), r.accumulation, r.smart), reverse=True)
    if not cand:
        await update.message.reply_text("🧱 바닥매집 후보 없음")
        return
    lines = ["🧱 <b>A100 v30 BOTTOM ACCUMULATION</b>", "과열 낮고 매집 흔적 있는 후보\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")



# ===== A100 v30 뉴스/전쟁/고래 AI =====
NEWS_CACHE = {}
NEWS_TTL = int(os.getenv("NEWS_TTL", "900"))

def text_hits(text, words):
    t = (text or "").lower()
    return sum(1 for w in words if w.lower() in t)

def rss_fetch_titles(name, url, ttl=NEWS_TTL):
    key = ("rss", name, url)
    old = NEWS_CACHE.get(key)
    if old and now_ts() - old[0] <= ttl:
        return old[1]
    titles = []
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "A100Bot/1.0"})
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.text)
            for item in root.findall(".//item")[:20]:
                title = item.findtext("title") or ""
                desc = item.findtext("description") or ""
                titles.append((title + " " + desc)[:500])
            NEWS_CACHE[key] = (now_ts(), titles)
            return titles
        log(f"rss {name} status {r.status_code}")
    except Exception as e:
        log(f"rss {name} err {e}")
    return old[1] if old else []

def v30_news_engine_base():
    feeds = [
        ("coindesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("cointelegraph", "https://cointelegraph.com/rss"),
        ("investing", "https://www.investing.com/rss/news_301.rss"),
    ]
    titles = []
    if os.getenv("AUTO_NEWS", "1") == "1":
        for name, url in feeds:
            titles += rss_fetch_titles(name, url)
    joined = " ".join(titles) + " " + os.getenv("MACRO_NOTE", "")

    risk_words = ["sec","lawsuit","hack","exploit","ban","sanction","liquidation","fed","powell","rate hike","inflation","tariff","default","소송","해킹","제재","금리","인플레이션","관세","청산"]
    bull_words = ["etf inflow","approval","rate cut","easing","institutional","adoption","승인","금리인하","유입","기관","채택"]
    war_words = ["iran","israel","russia","ukraine","taiwan","china","missile","attack","war","strike","red sea","houthi","이란","이스라엘","러시아","우크라이나","대만","중국","미사일","공격","전쟁","홍해"]
    whale_words = ["whale","large transfer","exchange inflow","exchange outflow","tether minted","usdt minted","bitcoin transfer","ethereum transfer","고래","대량이동","거래소 유입","거래소 유출","테더 발행"]

    risk_hit = text_hits(joined, risk_words)
    bull_hit = text_hits(joined, bull_words)
    war_hit = text_hits(joined, war_words)
    whale_hit = text_hits(joined, whale_words)

    news_risk = min(100, env_num("NEWS_RISK", 0) + risk_hit * 8 + war_hit * 4 - bull_hit * 4)
    war_risk = min(100, env_num("WAR_RISK", 0) + war_hit * 12)
    whale_risk = min(100, env_num("WHALE_RISK", 0) + whale_hit * 14)

    top_titles = []
    for t in titles[:10]:
        if text_hits(t, risk_words + bull_words + war_words + whale_words):
            top_titles.append(t[:140])

    return {
        "news_risk": round(max(0, news_risk), 1),
        "war_risk": round(max(0, war_risk), 1),
        "whale_risk": round(max(0, whale_risk), 1),
        "risk_hit": risk_hit,
        "bull_hit": bull_hit,
        "war_hit": war_hit,
        "whale_hit": whale_hit,
        "titles": top_titles[:5],
        "feed_count": len(titles),
    }

def v30_macro_engine():
    m = v30_base_macro_engine()
    n = v30_news_engine()
    risk = m["risk"]
    risk += min(n["news_risk"] * 0.25, 18)
    risk += min(n["war_risk"] * 0.22, 18)
    risk += min(n["whale_risk"] * 0.15, 12)
    risk = round(max(0, min(100, risk)), 1)

    events = list(m.get("events", []))
    if n["news_risk"] >= 60:
        events.append("뉴스위험 상승")
    if n["war_risk"] >= 60:
        events.append("전쟁/지정학 위험")
    if n["whale_risk"] >= 60:
        events.append("고래/거래소 이동 위험")

    if risk >= 78:
        mode, guard = "🔴 리스크오프", 16
    elif risk >= 62:
        mode, guard = "🟠 방어모드", 11
    elif risk >= 45:
        mode, guard = "🟡 보수모드", 6
    else:
        mode, guard = "🟢 일반모드", 0

    alt_penalty = m.get("alt_penalty", 0)
    if n["news_risk"] >= 50 or n["war_risk"] >= 50:
        alt_penalty += 6
    if n["whale_risk"] >= 60:
        alt_penalty += 4

    m.update({
        "risk": risk,
        "mode": mode,
        "guard": guard,
        "alt_penalty": alt_penalty,
        "events": events,
        "news_risk": n["news_risk"],
        "war": max(m.get("war", 0), n["war_risk"]),
        "whale": max(m.get("whale", 0), n["whale_risk"]),
        "news_ai": n,
    })
    return m

def macro_guard_add():
    return v30_macro_engine()["guard"]

def v26_macro_engine():
    return v30_macro_engine()

def v30_macro_report():
    m = v30_macro_engine()
    n = m.get("news_ai", {})
    ev = " / ".join(m["events"]) if m["events"] else "특이 이벤트 없음"
    titles = "\n".join([f"- {x}" for x in n.get("titles", [])]) or "- 주요 리스크 뉴스 없음"
    return (
        f"🌎 <b>A100 v30 NEWS/WAR/WHALE AI</b>\n"
        f"모드: <b>{m['mode']}</b>\n"
        f"종합위험: <b>{m['risk']}%</b> | 추천기준 +{m['guard']}점 | 알트감점 {m['alt_penalty']}점\n\n"
        f"일정: FOMC D-{int(m['fomc']) if m['fomc'] < 90 else '?'} / CPI D-{int(m['cpi']) if m['cpi'] < 90 else '?'} / PPI D-{int(m['ppi']) if m['ppi'] < 90 else '?'} / PCE D-{int(m['pce']) if m['pce'] < 90 else '?'} / NFP D-{int(m['nfp']) if m['nfp'] < 90 else '?'}\n"
        f"시장: FearGreed {m['fg']} / DXY {m['dxy']} / VIX {m['vix']} / BTC.D {m['btc_dom']} / USDT.D {m['usdt_dom']} / ETF {m['etf']}M\n"
        f"AI위험: 뉴스 {m.get('news_risk', m.get('news', 0))}% / 전쟁 {m['war']}% / 고래 {m['whale']}%\n"
        f"이벤트: {ev}\n"
        f"뉴스요약:\n{titles}\n\n"
        f"AI판정: {'FOMC/뉴스/전쟁 리스크 구간 — 알트 고배율 금지' if m['risk'] >= 60 else '일반 기준, 단 추격매수 금지'}"
    )

def v30_final_ai_score_base(r):
    base = real_signal_score(r)
    m = v30_macro_engine()
    major = r.sym.startswith(("BTC", "ETH"))
    s = base
    if not major:
        s -= m["alt_penalty"]
    if m["risk"] >= 75:
        s -= 10 if not major else 4
    elif m["risk"] >= 60:
        s -= 6 if not major else 2
    if m.get("news_risk", 0) >= 60 and not major:
        s -= 5
    if m["whale"] >= 60 and getattr(r, "smart", 0) >= 50:
        s += 3
    return round(clamp(s), 1)

async def macro_cmd(update,context):
    await update.message.reply_text(v30_macro_report(), parse_mode="HTML")

async def cgstatus_cmd(update,context):
    await update.message.reply_text(
        f"🧊 <b>CoinGlass Cache</b>\n"
        f"캐시 항목: {len(CG_CACHE)}개\n"
        f"TTL: {CG_CACHE_TTL}초\n"
        f"호출간격: {CG_MIN_INTERVAL}초\n"
        f"429 발생 시: 이전 캐시 우선 사용 권장",
        parse_mode="HTML"
    )



# ===== A100 v30 자동 매크로 수집 엔진 =====
AUTO_MACRO_CACHE = {}
AUTO_MACRO_TTL = int(os.getenv("AUTO_MACRO_TTL", "900"))

def http_json_cached(name, url, ttl=AUTO_MACRO_TTL, params=None, headers=None):
    key = (name, url, str(params), str(headers))
    old = AUTO_MACRO_CACHE.get(key)
    if old and now_ts() - old[0] <= ttl:
        return old[1]
    try:
        r = requests.get(url, params=params or {}, headers=headers or {}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            AUTO_MACRO_CACHE[key] = (now_ts(), data)
            return data
        log(f"auto macro http {name} {r.status_code} {r.text[:80]}")
    except Exception as e:
        log(f"auto macro err {name}: {e}")
    return old[1] if old else None

def auto_fear_greed():
    if os.getenv("AUTO_FEAR_GREED", "1") != "1":
        return env_num("FEAR_GREED", 50)
    data = http_json_cached("feargreed", "https://api.alternative.me/fng/")
    try:
        return safe_num(data["data"][0]["value"], env_num("FEAR_GREED", 50))
    except Exception:
        return env_num("FEAR_GREED", 50)

def auto_global_market():
    # CoinGecko 글로벌 데이터: BTC Dominance 자동
    if os.getenv("AUTO_MARKET", "1") != "1":
        return env_num("BTC_DOM_TREND", 0)
    data = http_json_cached("coingecko_global", "https://api.coingecko.com/api/v3/global")
    try:
        btc_dom = safe_num(data["data"]["market_cap_percentage"]["btc"], 50)
        # 50 기준 위면 BTC 흡성 위험으로 간주. trend 형식으로 변환.
        return round((btc_dom - 50) * 2, 1)
    except Exception:
        return env_num("BTC_DOM_TREND", 0)

def auto_events_days():
    # 완전 자동 일정 API가 없거나 제한될 수 있어, env 우선 + 기본 안전값.
    # V27은 AUTO_EVENTS_JSON 환경변수로 일정 일괄 입력 가능:
    # {"FOMC_DAYS":3,"CPI_DAYS":1,"PPI_DAYS":7,"PCE_DAYS":9,"NFP_DAYS":2,"GDP_DAYS":20}
    vals = {
        "FOMC_DAYS": env_num("FOMC_DAYS", 99),
        "CPI_DAYS": env_num("CPI_DAYS", 99),
        "PPI_DAYS": env_num("PPI_DAYS", 99),
        "PCE_DAYS": env_num("PCE_DAYS", 99),
        "NFP_DAYS": env_num("NFP_DAYS", 99),
        "GDP_DAYS": env_num("GDP_DAYS", 99),
    }
    try:
        import json as _json
        raw = os.getenv("AUTO_EVENTS_JSON", "").strip()
        if raw:
            obj = _json.loads(raw)
            for k in vals:
                if k in obj:
                    vals[k] = safe_num(obj[k], vals[k])
    except Exception as e:
        log(f"AUTO_EVENTS_JSON parse error {e}")
    return vals

def auto_news_risk():
    # 외부 뉴스 API 키 없이 안정 동작하도록 env 기반 + 키워드 메모 위험값 반영
    risk = env_num("NEWS_RISK", 0)
    memo = (os.getenv("MACRO_NOTE", "") or "").lower()
    hot_words = ["war", "attack", "iran", "israel", "russia", "ukraine", "taiwan", "tariff", "sec", "hack", "전쟁", "공격", "이란", "이스라엘", "러시아", "우크라이나", "대만", "관세", "해킹"]
    hit = sum(1 for w in hot_words if w in memo)
    return min(100, risk + hit * 8)

def v30_macro_engine():
    base_risk = env_num("MACRO_RISK", 35)
    note = os.getenv("MACRO_NOTE", "자동/수동 매크로 입력 없음")
    ev = auto_events_days()

    fomc = ev["FOMC_DAYS"]
    cpi = ev["CPI_DAYS"]
    ppi = ev["PPI_DAYS"]
    pce = ev["PCE_DAYS"]
    nfp = ev["NFP_DAYS"]
    gdp = ev["GDP_DAYS"]

    fg = auto_fear_greed()
    dxy = env_num("DXY_TREND", 0)
    vix = env_num("VIX_LEVEL", 15)
    btc_dom = auto_global_market()
    usdt_dom = env_num("USDT_DOM_TREND", 0)
    ten_y = env_num("US10Y_TREND", 0)
    etf = env_num("ETF_FLOW_M", 0)
    war = env_num("WAR_RISK", 0)
    news = auto_news_risk()
    whale = env_num("WHALE_RISK", 0)

    risk = base_risk
    event_msgs = []

    def add_event(days, name, d1, d3, d7=0):
        nonlocal risk
        if days <= 1:
            risk += d1
            event_msgs.append(f"{name} D-{int(days)} 고위험")
        elif days <= 3:
            risk += d3
            event_msgs.append(f"{name} D-{int(days)} 주의")
        elif days <= 7 and d7:
            risk += d7
            event_msgs.append(f"{name} D-{int(days)} 체크")

    add_event(fomc, "FOMC", 20, 12, 5)
    add_event(cpi, "CPI", 17, 9, 4)
    add_event(ppi, "PPI", 11, 6, 2)
    add_event(pce, "PCE", 14, 7, 3)
    add_event(nfp, "NFP", 14, 7, 3)
    add_event(gdp, "GDP", 9, 5, 2)

    risk += min(max(war, 0), 25)
    risk += min(max(news * 0.38, 0), 25)
    risk += min(max(whale * 0.20, 0), 15)

    if fg >= 82:
        risk += 13; event_msgs.append("Fear&Greed 극탐욕")
    elif fg >= 75:
        risk += 8; event_msgs.append("Fear&Greed 탐욕")
    elif fg <= 18:
        risk += 8; event_msgs.append("Fear&Greed 극공포")
    elif fg <= 28:
        risk += 4; event_msgs.append("Fear&Greed 공포")

    if dxy >= 30:
        risk += 12; event_msgs.append("DXY 강세")
    elif dxy <= -30:
        risk -= 5; event_msgs.append("DXY 약세")

    if vix >= 30:
        risk += 20; event_msgs.append("VIX 급등")
    elif vix >= 22:
        risk += 10; event_msgs.append("VIX 상승")

    if btc_dom >= 25:
        risk += 8; event_msgs.append("BTC 도미넌스 상승")
    elif btc_dom <= -25:
        risk -= 4; event_msgs.append("BTC 도미넌스 하락")

    if usdt_dom >= 25:
        risk += 10; event_msgs.append("USDT.D 상승")
    elif usdt_dom <= -25:
        risk -= 4; event_msgs.append("USDT.D 하락")

    if ten_y >= 30:
        risk += 8; event_msgs.append("미국채10Y 상승")
    elif ten_y <= -30:
        risk -= 3; event_msgs.append("미국채10Y 하락")

    if etf <= -300:
        risk += 12; event_msgs.append("ETF 대량 유출")
    elif etf >= 300:
        risk -= 8; event_msgs.append("ETF 대량 유입")

    risk = round(max(0, min(100, risk)), 1)

    if risk >= 78:
        mode = "🔴 리스크오프"
        guard = 15
    elif risk >= 62:
        mode = "🟠 방어모드"
        guard = 10
    elif risk >= 45:
        mode = "🟡 보수모드"
        guard = 5
    else:
        mode = "🟢 일반모드"
        guard = 0

    alt_penalty = 0
    if dxy >= 30 or btc_dom >= 25 or usdt_dom >= 25 or vix >= 22 or risk >= 60:
        alt_penalty += 7
    if war >= 50 or news >= 60 or whale >= 60:
        alt_penalty += 6

    return {
        "risk": risk, "mode": mode, "guard": guard, "alt_penalty": alt_penalty,
        "note": note, "events": event_msgs,
        "fomc": fomc, "cpi": cpi, "ppi": ppi, "pce": pce, "nfp": nfp, "gdp": gdp,
        "fg": fg, "dxy": dxy, "vix": vix, "btc_dom": btc_dom, "usdt_dom": usdt_dom, "us10y": ten_y,
        "etf": etf, "war": war, "news": news, "whale": whale,
    }

# V27에서는 기존 v26 엔진을 자동 엔진으로 대체
def v26_macro_engine():
    return v30_base_macro_engine()

def macro_guard_add():
    return v30_macro_engine()["guard"]

def v30_base_macro_report():
    m = v30_base_macro_engine()
    ev = " / ".join(m["events"]) if m["events"] else "특이 이벤트 없음"
    return (
        f"🌎 <b>A100 v30 AUTO MACRO LIVE</b>\n"
        f"모드: <b>{m['mode']}</b>\n"
        f"종합위험: <b>{m['risk']}%</b> | 추천기준 +{m['guard']}점 | 알트감점 {m['alt_penalty']}점\n\n"
        f"일정: FOMC D-{int(m['fomc']) if m['fomc'] < 90 else '?'} / CPI D-{int(m['cpi']) if m['cpi'] < 90 else '?'} / PPI D-{int(m['ppi']) if m['ppi'] < 90 else '?'} / PCE D-{int(m['pce']) if m['pce'] < 90 else '?'} / NFP D-{int(m['nfp']) if m['nfp'] < 90 else '?'} / GDP D-{int(m['gdp']) if m['gdp'] < 90 else '?'}\n"
        f"시장: FearGreed {m['fg']} / DXY {m['dxy']} / VIX {m['vix']} / BTC.D {m['btc_dom']} / USDT.D {m['usdt_dom']} / US10Y {m['us10y']} / ETF {m['etf']}M\n"
        f"지정학: 전쟁 {m['war']}% / 뉴스위험 {m['news']}% / 고래위험 {m['whale']}%\n"
        f"이벤트: {ev}\n"
        f"메모: {m['note']}\n\n"
        f"AI판정: {'알트 고배율 금지 / BTC·ETH 우선 / 손절 짧게' if m['risk'] >= 60 else '일반 기준, 단 추격매수 금지'}"
    )

async def events_cmd(update,context):
    m = v30_base_macro_engine()
    text = (
        "📅 <b>A100 v30 주요 이벤트</b>\n"
        f"FOMC D-{int(m['fomc']) if m['fomc'] < 90 else '?'}\n"
        f"CPI D-{int(m['cpi']) if m['cpi'] < 90 else '?'}\n"
        f"PPI D-{int(m['ppi']) if m['ppi'] < 90 else '?'}\n"
        f"PCE D-{int(m['pce']) if m['pce'] < 90 else '?'}\n"
        f"NFP D-{int(m['nfp']) if m['nfp'] < 90 else '?'}\n"
        f"GDP D-{int(m['gdp']) if m['gdp'] < 90 else '?'}\n\n"
        "AUTO_EVENTS_JSON 또는 FOMC_DAYS, CPI_DAYS, PPI_DAYS, PCE_DAYS, NFP_DAYS 값을 넣으면 자동 반영됩니다."
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def macrohelp_cmd(update,context):
    text = (
        "🛠 <b>V26 매크로 입력값</b>\n"
        "Render → Environment에 아래 KEY 추가/수정\n\n"
        "MACRO_RISK = 35\n"
        "FOMC_DAYS = 3\n"
        "CPI_DAYS = 1\n"
        "PPI_DAYS = 99\n"
        "PCE_DAYS = 99\n"
        "NFP_DAYS = 99\n"
        "GDP_DAYS = 99\n"
        "WAR_RISK = 0~100\n"
        "NEWS_RISK = 0~100\n"
        "FEAR_GREED = 0~100\n"
        "DXY_TREND = -100~100\n"
        "VIX_LEVEL = 15\n"
        "BTC_DOM_TREND = -100~100\n"
        "ETF_FLOW_M = 백만달러 단위\n"
        "MACRO_NOTE = 메모"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def live_cmd(update,context):
    m = v30_macro_engine()
    n = m.get("news_ai", {})
    text = (
        "📡 <b>A100 v30 LIVE DATA</b>\n"
        f"Fear&Greed: {m['fg']} {'(자동)' if os.getenv('AUTO_FEAR_GREED','1')=='1' else '(수동)'}\n"
        f"BTC Dominance Trend: {m['btc_dom']} {'(자동)' if os.getenv('AUTO_MARKET','1')=='1' else '(수동)'}\n"
        f"News Feed: {n.get('feed_count', 0)}개 / NewsRisk {m.get('news_risk', 0)}% / War {m['war']}% / Whale {m['whale']}%\n"
        f"Macro Cache: {len(AUTO_MACRO_CACHE)}개 / News Cache: {len(NEWS_CACHE)}개\n"
        f"Risk: {m['risk']}% / Mode: {m['mode']}"
    )
    await update.message.reply_text(text, parse_mode="HTML")



# ===== A100 v30 한글 뉴스 요약 / 영향도 / 메타스코어 =====
SEEN_NEWS = set()

def ko_news_title(t):
    raw = (t or "").strip()
    low = raw.lower()
    rules = [
        ("swift", "Swift, 글로벌 은행용 블록체인 결제망 관련 뉴스"),
        ("stablecoin", "스테이블코인 관련 뉴스"),
        ("etf", "ETF 자금/승인 관련 뉴스"),
        ("sec", "미 SEC 규제 관련 뉴스"),
        ("lawsuit", "소송/규제 리스크 관련 뉴스"),
        ("hack", "해킹/보안 사고 관련 뉴스"),
        ("exploit", "취약점 공격 관련 뉴스"),
        ("fomc", "FOMC 금리 이벤트 관련 뉴스"),
        ("powell", "파월/Fed 발언 관련 뉴스"),
        ("inflation", "인플레이션 지표 관련 뉴스"),
        ("iran", "이란 지정학 리스크 관련 뉴스"),
        ("israel", "이스라엘/중동 지정학 리스크 관련 뉴스"),
        ("russia", "러시아 지정학 리스크 관련 뉴스"),
        ("ukraine", "우크라이나 전쟁 리스크 관련 뉴스"),
        ("whale", "고래 대량 이동 관련 뉴스"),
        ("tether", "USDT/테더 유동성 관련 뉴스"),
        ("binance", "바이낸스 관련 뉴스"),
        ("coinbase", "코인베이스 관련 뉴스"),
        ("solana", "솔라나 생태계 관련 뉴스"),
        ("ethereum", "이더리움 관련 뉴스"),
        ("bitcoin", "비트코인 관련 뉴스"),
    ]
    for k, v in rules:
        if k in low:
            return v
    return raw[:90] + ("..." if len(raw) > 90 else "")

def news_sentiment_impact(t):
    low = (t or "").lower()
    pos_words = ["approval","approved","inflow","rate cut","easing","partnership","adoption","record high","launch","integrates","승인","유입","금리인하","채택","협력"]
    neg_words = ["hack","exploit","lawsuit","sec","ban","outflow","war","attack","missile","sanction","rate hike","inflation hot","liquidation","해킹","소송","제재","전쟁","공격","유출","청산"]
    war_words = ["iran","israel","russia","ukraine","taiwan","missile","attack","war","strike","이란","이스라엘","러시아","우크라이나","대만","미사일","공격","전쟁"]
    whale_words = ["whale","large transfer","exchange inflow","exchange outflow","tether minted","usdt minted","고래","대량이동","거래소 유입","거래소 유출","테더 발행"]
    score = 50
    score += text_hits(low, pos_words) * 12
    score -= text_hits(low, neg_words) * 12
    if text_hits(low, war_words):
        score -= 18
    if text_hits(low, whale_words):
        score -= 5
    score = max(0, min(100, score))
    if score >= 65:
        label = "🟢 호재"; market = "긍정"
    elif score <= 38:
        label = "🔴 악재/주의"; market = "부정"
    else:
        label = "🟡 중립"; market = "중립"
    impact = min(5, max(1, int(abs(score - 50) / 10) + 1))
    return score, label, market, "★" * impact + "☆" * (5 - impact)

def related_coins(t):
    low = (t or "").lower()
    coins = []
    mapping = {
        "bitcoin": "BTC", "btc": "BTC", "ethereum": "ETH", "eth": "ETH",
        "solana": "SOL", "sol": "SOL", "xrp": "XRP", "ripple": "XRP",
        "chainlink": "LINK", "link": "LINK", "ondo": "ONDO",
        "stablecoin": "ETH/ONDO/LINK", "tether": "USDT/BTC", "usdt": "USDT/BTC",
        "swift": "LINK/XRP/ETH", "binance": "BNB/BTC", "coinbase": "BTC/ETH", "etf": "BTC/ETH",
    }
    for k, v in mapping.items():
        if k in low and v not in coins:
            coins.append(v)
    return ", ".join(coins[:5]) if coins else "BTC/ETH"

def summarize_ko(t):
    low = (t or "").lower()
    bullets = []
    if "etf" in low:
        bullets.append("ETF 자금 흐름 또는 승인 이슈가 시장 심리에 영향")
    if "sec" in low or "lawsuit" in low:
        bullets.append("규제/소송 리스크로 알트코인 변동성 확대 가능")
    if "fomc" in low or "powell" in low or "fed" in low:
        bullets.append("금리 기대 변화로 BTC와 알트 전체 변동성 확대 가능")
    if any(w in low for w in ["iran","israel","russia","ukraine","war","attack","missile"]):
        bullets.append("지정학 리스크 상승 시 리스크오프 가능성")
    if any(w in low for w in ["whale","large transfer","exchange inflow","exchange outflow"]):
        bullets.append("고래/거래소 이동은 단기 매도압 또는 수급 변화를 의미")
    if "stablecoin" in low or "swift" in low:
        bullets.append("스테이블코인·결제 인프라 확대는 중장기 호재 가능")
    if not bullets:
        bullets.append("시장 심리에 영향을 줄 수 있는 일반 뉴스")
    bullets.append("단기 매매는 차트·거래량·파생수급 확인 필요")
    return bullets[:3]

def normalize_news_key(t):
    s = re.sub(r"[^a-zA-Z0-9가-힣 ]", "", (t or "").lower())
    return " ".join(s.split()[:10])

def v30_news_engine():
    n = v30_news_engine_base()
    raw = []
    try:
        for key, val in NEWS_CACHE.items():
            if isinstance(key, tuple) and key and key[0] == "rss":
                raw += val[1]
    except Exception:
        pass
    if not raw:
        raw = n.get("titles", [])
    n["raw_titles"] = raw
    return n

def important_news_items(limit=5):
    n = v30_news_engine()
    items = []
    for t in n.get("raw_titles", [])[:30]:
        key = normalize_news_key(t)
        if not key or key in SEEN_NEWS:
            continue
        score, label, market, stars_ = news_sentiment_impact(t)
        importance = abs(score - 50) + text_hits(t, ["fomc","cpi","etf","sec","hack","war","attack","whale","fed","powell","iran","israel"]) * 8
        if importance < 18:
            continue
        items.append((importance, t, score, label, market, stars_))
    items = sorted(items, reverse=True)[:limit]
    for _, t, *_ in items:
        SEEN_NEWS.add(normalize_news_key(t))
    return items

def format_news_ko(t, idx=1):
    score, label, market, stars_ = news_sentiment_impact(t)
    title = ko_news_title(t)
    coins = related_coins(t)
    bullets = summarize_ko(t)
    action = "관망/리스크 관리" if score < 45 else "관심 유지" if score < 65 else "관련 섹터 관심"
    return (
        f"📰 <b>{idx}. {title}</b>\n"
        f"AI판정: <b>{label}</b> | 시장영향: {market} | 영향도 {stars_}\n"
        f"관련코인: {coins}\n"
        f"요약:\n"
        f"- {bullets[0]}\n"
        f"- {bullets[1] if len(bullets)>1 else '추가 확인 필요'}\n"
        f"추천행동: {action}\n"
    )

def v30_meta_score(r):
    base = v30_final_ai_score_base(r)
    macro = v30_macro_engine()
    major = r.sym.startswith(("BTC", "ETH"))
    s = base
    s += min(max(timing_score(r) - 45, 0), 10) * 0.4
    s += min(max(breakout_score(r) - 35, 0), 10) * 0.3
    s += min(max(whale_score(r) - 40, 0), 10) * 0.2
    if macro["risk"] >= 70 and not major:
        s -= 8
    if macro["risk"] <= 40:
        s += 3
    if macro.get("news_risk", 0) >= 65 and not major:
        s -= 5
    return round(clamp(s), 1)

def v30_market_mode():
    m = v30_macro_engine()
    risk = m["risk"]; fg = m.get("fg", 50)
    if risk >= 82:
        return "⚫ Crash"
    if risk >= 70:
        return "🔴 Panic"
    if risk >= 55 and fg >= 65:
        return "🟠 Distribution"
    if risk <= 45 and fg < 75:
        return "🟢 Bull/Recovery"
    return "🟡 Rotation"

async def news_cmd(update,context):
    n = v30_news_engine()
    items = important_news_items(5)
    if not items:
        raw = n.get("raw_titles", [])[:5]
        items = [(20, t, *news_sentiment_impact(t)) for t in raw]
    lines = [
        "📰 <b>A100 v30 한글 뉴스 AI</b>",
        f"뉴스위험 {n['news_risk']}% | 전쟁위험 {n['war_risk']}% | 고래위험 {n['whale_risk']}%",
        f"Feed {n['feed_count']}개 | 중요 뉴스 선별\n",
    ]
    for i, item in enumerate(items[:5], 1):
        t = item[1]
        lines.append(format_news_ko(t, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def final_cmd(update,context):
    await update.message.reply_text("🧠 A100 v30 메타 AI 점수 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    res = sorted(res, key=lambda r: (v30_meta_score(r), timing_score(r), breakout_score(r)), reverse=True)
    lines = ["🧠 <b>A100 v30 META AI RANK</b>", f"시장모드: <b>{v30_market_mode()}</b> / 매크로위험 {v30_macro_engine()['risk']}%", ""]
    for i, r in enumerate(res[:10], 1):
        decision_fn = globals().get("v25_decision") or globals().get("v24_decision") or globals().get("v23_decision")
        decision = decision_fn(r) if decision_fn else "대기"
        lines.append(
            f"{i}. <b>{r.sym}</b> {stars(v30_meta_score(r))}\n"
            f"메타AI {v30_meta_score(r)}% | 실전 {real_signal_score(r)}% | 타이밍 {timing_score(r)}% | 돌파 {breakout_score(r)}% | 추격위험 {chase_risk(r)}%\n"
            f"판정: {decision}\n"
        )
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def mode_cmd(update,context):
    await update.message.reply_text(
        f"🧭 <b>A100 v30 시장모드</b>\n"
        f"현재: <b>{v30_market_mode()}</b>\n"
        f"매크로위험: {v30_macro_engine()['risk']}%\n"
        f"추천: {'고배율 금지 / 관망 우선' if v30_macro_engine()['risk'] >= 60 else '일반 기준 / 추격매수 금지'}",
        parse_mode="HTML"
    )

def main():
    if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN 필요")
    threading.Thread(target=health,daemon=True).start()
    sch=BackgroundScheduler(timezone="Asia/Seoul"); sch.add_job(morning,CronTrigger(hour=5,minute=0)); sch.add_job(alert,"interval",minutes=30); sch.start()
    try: asyncio.get_running_loop()
    except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
    app=Application.builder().token(BOT_TOKEN).build()
    for name,fn in [("start",start),("help",start),("myid",myid),("check",check),("scan",scan_cmd),("rank",rank_cmd),("best",rank_cmd),("top",rank_cmd),("hot",hot_cmd),("sniper",sniper_cmd),("elite",elite_cmd),("only",only_cmd),("auto",auto_cmd),("god",god_cmd),("real",real_cmd),("scalp",scalp_cmd),("tenx",tenx_cmd),("breakout",breakout_cmd),("bottom",bottom_cmd),("timing",timing_cmd),("now",now_cmd),("win",win_cmd),("smart",smart_cmd),("danger",danger_cmd),("watch",watch_cmd),("risk",risk_cmd),("kr",kr_cmd),("cgtest",cgtest_cmd),("macro",macro_cmd),("cgstatus",cgstatus_cmd),("events",events_cmd),("macrohelp",macrohelp_cmd),("live",live_cmd),("news",news_cmd),("final",final_cmd),("mode",mode_cmd)]:
        app.add_handler(CommandHandler(name,fn))
    log("A100 v30 Korean News Meta AI worker running..."); app.run_polling()
if __name__=="__main__": main()
