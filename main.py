
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
        b=b"A100 v22 God Mode running"; self.send_response(200); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
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

def god_score(r):
    # 최종 GOD 점수: 폭발·타이밍·10배후보·승률 종합
    g = (
        explosion_score(r) * 0.20
        + timing_score(r) * 0.20
        + quality_score(r) * 0.18
        + tenx_score(r) * 0.18
        + whale_score(r) * 0.12
        + win_rate_estimate(r) * 0.12
    )
    g -= 15 if r.bubble >= 70 or r.distribution >= 70 else 0
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
        f"GOD {god_score(r)}% | 10X {tenx_score(r)}% | 타이밍 {timing_score(r)}% | 승률 {win_rate_estimate(r)}% | RR {rr_score(r)}\n"
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
    lines = ["⚡ <b>A100 v22 Adaptive Signal Rank</b>", market_header(), "추천품질·폭발확률 기준으로 재정렬\n"]
    for i, r in enumerate(ranked[:n], 1):
        lines.append(format_elite(r, i))
    return "\n".join(lines) if ranked else "A100 후보 없음"

def report(symbols,n=10):
    res=scan(symbols)
    return "A100 결과 없음" if not res else "🔥 <b>A100 v22 God Mode</b>\n폭발확률·추천품질 중심 분석\n\n"+"\n━━━━━━━━━━━━\n".join(full(r) for r in elite_sort(res)[:n])

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE): await update.message.reply_text("A100 v22 시작\n/check\n/scan ARKM,SYN,SENT\n/rank\n/hot\n/sniper\n/elite\n/only\n/god\n/tenx\n/breakout\n/bottom\n/timing\n/now\n/win ARKM,SYN\n/smart\n/danger\n/watch\n/risk ARKM,SYN\n/kr\n/cgtest BTC\n/myid")
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
    await update.message.reply_text("🎯 A100 v22 스나이퍼 단일 후보 스캔 중...")
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
        "🎯 <b>A100 v22 SNIPER PICK</b>\n\n"
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
    await update.message.reply_text("🏆 A100 v22 Elite Pick TOP5 스캔 중...")
    res = elite_sort(scan(top_usdt(TOP_SCAN_LIMIT)))
    if not res:
        await update.message.reply_text("🏆 A100 ELITE\n\n오늘은 Elite 후보가 없습니다.\n무리한 진입보다 기다리는 것이 유리합니다.")
        return
    lines = ["🏆 <b>A100 v22 ELITE PICK TOP5</b>", market_header(), ""]
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
def morning(): send("🌅 <b>A100 v22 오전 5시 Elite 리포트</b>\n\n"+report(DEFAULT_SYMBOLS,10))
def alert():
    hit=[r for r in scan(DEFAULT_SYMBOLS) if strict_pass(r) and (r.score>=SCORE_ALERT or r.accumulation>=80 or r.smart>=75 or r.squeeze>=75 or timing_score(r)>=72 or god_score(r)>=70)]
    if hit: send("🚨 <b>A100 v22 조건 감지</b>\n\n"+ranktxt(hit,5))



async def god_cmd(update,context):
    await update.message.reply_text("🔥 A100 v22 GOD 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if god_pass(r)]
    cand = sorted(cand, key=lambda r: (god_score(r), tenx_score(r), timing_score(r), win_rate_estimate(r)), reverse=True)
    if not cand:
        await update.message.reply_text("🔥 GOD 후보 없음\n\n기준 미달이면 억지 추천하지 않습니다.")
        return
    lines = ["🔥 <b>A100 v22 GOD MODE</b>", market_header(), "폭발·타이밍·10X·고래수급 종합\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def tenx_cmd(update,context):
    await update.message.reply_text("💎 A100 10X 잠재 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if tenx_score(r) >= 48 and r.bubble < 70 and r.distribution < 70]
    cand = sorted(cand, key=lambda r: (tenx_score(r), bottom_score(r), whale_score(r)), reverse=True)
    if not cand:
        await update.message.reply_text("💎 10X 잠재 후보 없음")
        return
    lines = ["💎 <b>A100 10X WATCH</b>", "초고위험 장기 잠재 후보입니다. 단타 매수신호가 아닙니다.\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def breakout_cmd(update,context):
    await update.message.reply_text("🚀 A100 돌파직전 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if breakout_score(r) >= 45 and r.bubble < 75 and r.distribution < 75]
    cand = sorted(cand, key=lambda r: (breakout_score(r), timing_score(r), r.squeeze), reverse=True)
    if not cand:
        await update.message.reply_text("🚀 돌파직전 후보 없음")
        return
    lines = ["🚀 <b>A100 BREAKOUT WATCH</b>", "저항 근접·거래량·스퀴즈 기준\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def bottom_cmd(update,context):
    await update.message.reply_text("🧱 A100 바닥매집 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if bottom_score(r) >= 55 and r.accumulation >= 45 and r.bubble < 65]
    cand = sorted(cand, key=lambda r: (bottom_score(r), r.accumulation, r.smart), reverse=True)
    if not cand:
        await update.message.reply_text("🧱 바닥매집 후보 없음")
        return
    lines = ["🧱 <b>A100 BOTTOM ACCUMULATION</b>", "과열 낮고 매집 흔적 있는 후보\n"]
    for i, r in enumerate(cand[:10], 1):
        lines.append(format_god(r, i))
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def timing_cmd(update,context):
    await update.message.reply_text("⏱ A100 v22 진입 타이밍 후보 스캔 중...")
    res = scan(top_usdt(TOP_SCAN_LIMIT))
    cand = [r for r in res if timing_pass(r)]
    cand = sorted(cand, key=lambda r: (timing_score(r), quality_score(r), win_rate_estimate(r)), reverse=True)
    if not cand:
        await update.message.reply_text("⏱ 지금 진입 타이밍 후보 없음\n\n기준 미달이면 기다리는 것이 유리합니다.")
        return
    lines = ["⏱ <b>A100 v22 TIMING AI</b>", market_header(), "지금 자리 기준 랭킹\n"]
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
        "🚨 <b>A100 v22 NOW ENTRY</b>\n\n"
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
    lines = ["📊 <b>A100 v22 예상승률 TOP</b>\n"]
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


def main():
    if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN 필요")
    threading.Thread(target=health,daemon=True).start()
    sch=BackgroundScheduler(timezone="Asia/Seoul"); sch.add_job(morning,CronTrigger(hour=5,minute=0)); sch.add_job(alert,"interval",minutes=30); sch.start()
    try: asyncio.get_running_loop()
    except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
    app=Application.builder().token(BOT_TOKEN).build()
    for name,fn in [("start",start),("help",start),("myid",myid),("check",check),("scan",scan_cmd),("rank",rank_cmd),("best",rank_cmd),("top",rank_cmd),("hot",hot_cmd),("sniper",sniper_cmd),("elite",elite_cmd),("only",only_cmd),("god",god_cmd),("tenx",tenx_cmd),("breakout",breakout_cmd),("bottom",bottom_cmd),("timing",timing_cmd),("now",now_cmd),("win",win_cmd),("smart",smart_cmd),("danger",danger_cmd),("watch",watch_cmd),("risk",risk_cmd),("kr",kr_cmd),("cgtest",cgtest_cmd)]:
        app.add_handler(CommandHandler(name,fn))
    log("A100 v22 God Mode worker running..."); app.run_polling()
if __name__=="__main__": main()
