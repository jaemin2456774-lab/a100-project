
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
        b=b"A100 v17 Clean Core running"; self.send_response(200); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
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
def ranktxt(res,n=10):
    lines=["⚡ <b>A100 v17 빠른 신호 랭킹</b>\n"]
    for i,r in enumerate(res[:n],1):
        lines.append(f"{i}. <b>{r.sym}</b> {stars(r.score)}\n점수 {r.score} | 매집 {r.accumulation}% | 스마트 {r.smart}% | 스퀴즈 {r.squeeze}% | 신뢰 {r.confidence}%\n판정: <b>{r.action}</b> | 단계: {r.stage}\n진입 <code>{r.entry_low}~{r.entry_high}</code> / 손절 <code>{r.stop}</code> / 목표 <code>{r.target1}</code>\n이유: {r.reason}\n")
    return "\n".join(lines)
def report(symbols,n=10):
    res=scan(symbols)
    return "A100 결과 없음" if not res else "🔥 <b>A100 v17 Clean Core</b>\n\n"+"\n━━━━━━━━━━━━\n".join(full(r) for r in res[:n])

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE): await update.message.reply_text("A100 v17 시작\n/check\n/scan ARKM,SYN,SENT\n/rank\n/hot\n/risk ARKM,SYN\n/kr\n/cgtest BTC\n/myid")
async def myid(update,context): await update.message.reply_text(f"TELEGRAM_CHAT_ID = {update.effective_chat.id}")
async def check(update,context): await update.message.reply_text("A100 분석 중..."); await update.message.reply_text(report(DEFAULT_SYMBOLS,10),parse_mode="HTML")
async def scan_cmd(update,context):
    raw=" ".join(context.args).strip()
    if not raw: await update.message.reply_text("예: /scan ARKM,SYN,SENT"); return
    syms=[x.strip().upper() for x in raw.replace(" ","").split(",") if x.strip()]
    await update.message.reply_text("A100 분석 중..."); await update.message.reply_text(report(syms,10),parse_mode="HTML")
async def rank_cmd(update,context): await update.message.reply_text("A100 랭킹 스캔 중..."); await update.message.reply_text(ranktxt(scan(top_usdt(TOP_SCAN_LIMIT)),15),parse_mode="HTML")
async def hot_cmd(update,context):
    await update.message.reply_text("A100 HOT 후보 스캔 중..."); res=scan(top_usdt(TOP_SCAN_LIMIT)); hot=[r for r in res if r.accumulation>=55 and r.confidence>=35 and r.bubble<75 and r.distribution<75]
    await update.message.reply_text(ranktxt(hot,10) if hot else "HOT 후보 없음",parse_mode="HTML")
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
def morning(): send("🌅 <b>A100 오전 5시 리포트</b>\n\n"+report(DEFAULT_SYMBOLS,10))
def alert():
    hit=[r for r in scan(DEFAULT_SYMBOLS) if r.score>=SCORE_ALERT or r.accumulation>=80 or r.smart>=75 or r.squeeze>=75]
    if hit: send("🚨 <b>A100 조건 감지</b>\n\n"+ranktxt(hit,5))
def main():
    if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN 필요")
    threading.Thread(target=health,daemon=True).start()
    sch=BackgroundScheduler(timezone="Asia/Seoul"); sch.add_job(morning,CronTrigger(hour=5,minute=0)); sch.add_job(alert,"interval",minutes=30); sch.start()
    try: asyncio.get_running_loop()
    except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
    app=Application.builder().token(BOT_TOKEN).build()
    for name,fn in [("start",start),("help",start),("myid",myid),("check",check),("scan",scan_cmd),("rank",rank_cmd),("best",rank_cmd),("top",rank_cmd),("hot",hot_cmd),("risk",risk_cmd),("kr",kr_cmd),("cgtest",cgtest_cmd)]:
        app.add_handler(CommandHandler(name,fn))
    log("A100 v17 Clean Core worker running..."); app.run_polling()
if __name__=="__main__": main()
