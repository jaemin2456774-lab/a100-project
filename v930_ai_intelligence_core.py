"""A100 V93.0 AI Intelligence Core.
Pure, dependency-free decision helpers. No network, Telegram, state writes, or order path.
Schema-1 compatible by design: consumes existing dictionaries and returns derived views only.
"""
from __future__ import annotations
from collections import Counter

ENGINE_KEYS = ("Pattern", "Liquidity", "Momentum", "Market", "Risk", "Timing", "Learning", "Meta")

def clamp(v, lo=0.0, hi=100.0):
    try: return max(lo, min(hi, float(v)))
    except Exception: return lo

def classify_regime(item: dict) -> dict:
    c=item.get("components") or {}
    momentum=clamp(c.get("Momentum",50)); market=clamp(c.get("Market",50)); risk=clamp(c.get("Risk",50)); timing=clamp(c.get("Timing",50))
    spread=abs(momentum-market)
    if risk < 38: name="PANIC"
    elif momentum >= 72 and timing >= 65: name="BREAKOUT"
    elif momentum >= 60 and market >= 58: name="TREND"
    elif spread <= 10 and 42 <= momentum <= 60: name="RANGE"
    else: name="RECOVERY"
    confidence=clamp(55 + abs(momentum-50)*0.45 + abs(market-50)*0.25 + (50-risk)*0.20, 45, 95)
    return {"name":name,"confidence":round(confidence,1),"momentum":momentum,"market":market,"risk":risk,"timing":timing}

def adaptive_weights(item: dict, memory: dict | None=None) -> dict:
    c=item.get("components") or {}; memory=memory or {}; completion=clamp(memory.get("completion",0))
    base={"Pattern":1.20,"Liquidity":1.00,"Momentum":1.00,"Market":1.05,"Risk":1.25,"Timing":1.10,"Learning":0.65,"Meta":1.15}
    regime=classify_regime(item)["name"]
    if regime=="BREAKOUT": base.update(Momentum=1.30,Timing=1.30,Liquidity=1.15)
    elif regime=="TREND": base.update(Pattern=1.30,Market=1.20,Momentum=1.15)
    elif regime=="RANGE": base.update(Risk=1.40,Timing=1.25,Momentum=0.80)
    elif regime=="PANIC": base.update(Risk=1.60,Liquidity=1.25,Timing=0.80)
    else: base.update(Pattern=1.15,Risk=1.35,Learning=0.80)
    base["Learning"] *= 0.35 + 0.65*(completion/100.0)
    total=sum(base.values()) or 1
    return {k:round(v/total*100,1) for k,v in base.items() if k in c or k in {"Risk","Learning"}}

def engine_contributions(item: dict, memory: dict | None=None) -> list[dict]:
    c=item.get("components") or {}; weights=adaptive_weights(item,memory); rows=[]
    for k,w in weights.items():
        score=clamp(c.get(k,50)); contribution=(score-50.0)*(w/100.0)
        rows.append({"engine":k,"score":round(score,1),"weight":w,"contribution":round(contribution,1)})
    return sorted(rows,key=lambda x:abs(x["contribution"]),reverse=True)

def strategy_for_regime(regime: str) -> str:
    return {"BREAKOUT":"Momentum Breakout","TREND":"Trend Follow","RANGE":"Mean Reversion / Wait","PANIC":"Capital Defense","RECOVERY":"Selective Recovery"}.get(regime,"Balanced")

def summarize_history(rows: list[dict]) -> dict:
    windows={}
    for n in (50,100,300):
        sample=rows[-n:]
        vals=[]
        for r in sample:
            try: vals.append(float(r.get("return_pct",r.get("pnl_pct",r.get("result_pct",0))) or 0))
            except Exception: pass
        wins=sum(v>0 for v in vals)
        windows[n]={"n":len(vals),"win_rate":round(wins/len(vals)*100,1) if vals else 0.0,"avg":round(sum(vals)/len(vals),2) if vals else 0.0}
    losses=[str(r.get("close_reason") or r.get("reason") or "unknown") for r in rows if float(r.get("return_pct",r.get("pnl_pct",0)) or 0)<=0]
    return {"windows":windows,"top_loss_reasons":Counter(losses).most_common(3)}

def build_core(item: dict, decision: dict, history: list[dict] | None=None) -> dict:
    memory=decision.get("memory") or {}; regime=classify_regime(item); contrib=engine_contributions(item,memory)
    positive=[x for x in contrib if x["contribution"]>0.5]; negative=[x for x in contrib if x["contribution"]<-0.5]
    verdict=str(decision.get("verdict","WATCH")).upper(); symbol=str(item.get("symbol","?")); side=str(item.get("side","?"))
    why=[]
    if positive: why.append("지지 엔진: "+", ".join(x["engine"] for x in positive[:3]))
    if negative: why.append("억제 엔진: "+", ".join(x["engine"] for x in negative[:3]))
    why.append(f"시장 국면 {regime['name']}에 {strategy_for_regime(regime['name'])} 전략 적용")
    risks=list(decision.get("risks") or [])
    explanation=f"{symbol} {side}는 {why[0] if why else '뚜렷한 우위가 부족'}합니다. "
    explanation += f"현재 시장은 {regime['name']}({regime['confidence']:.0f}%)로 분류되어 {verdict} 판정을 유지합니다."
    return {"version":"V93.0","verdict":verdict,"regime":regime,"strategy":strategy_for_regime(regime["name"]),"weights":adaptive_weights(item,memory),"contributions":contrib,"explanation":explanation,"why":why,"risks":risks,"history":summarize_history(history or [])}
