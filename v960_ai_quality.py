"""A100 V96.0 AI Quality & Similarity analytics.
Pure analytics only: no network, scheduler, state mutation, or order execution.
Consumes existing schema-1 dictionaries and returns derived views.
"""
from __future__ import annotations
from math import sqrt

ENGINE_KEYS=("Pattern","Liquidity","Momentum","Market","Risk","Timing","Learning","Meta")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def clamp(v,lo=0.0,hi=100.0):return max(lo,min(hi,_f(v)))

def row_return(row):
    for k in ("realized_pct","return_pct","pnl_pct","result_pct"):
        if k in row:return _f(row.get(k))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p

def _components(obj):
    c=obj.get("components") or obj.get("engine_scores") or obj.get("scores") or {}
    return c if isinstance(c,dict) else {}

def component_similarity(item,row):
    a=_components(item); b=_components(row)
    common=[k for k in ENGINE_KEYS if k in a and k in b]
    if not common:return 0.0
    dist=sqrt(sum((_f(a[k],50)-_f(b[k],50))**2 for k in common)/len(common))
    return round(clamp(100-dist*2.0),1)

def find_similar(item,rows,limit=12,min_score=55.0):
    symbol=str(item.get("symbol","")).upper(); side=str(item.get("side","")).upper()
    ranked=[]
    for r in rows:
        score=component_similarity(item,r)
        if score<=0:continue
        bonus=0.0
        if str(r.get("symbol","")).upper()==symbol:bonus+=8
        if str(r.get("side","")).upper()==side:bonus+=6
        total=clamp(score+bonus)
        if total>=min_score:ranked.append((total,r))
    ranked.sort(key=lambda x:x[0],reverse=True)
    selected=ranked[:max(1,int(limit))]
    vals=[row_return(r) for _,r in selected]
    wins=sum(v>0 for v in vals); n=len(vals)
    return {"n":n,"win_rate":round(wins/n*100,1) if n else 0.0,
            "avg":round(sum(vals)/n,2) if n else 0.0,
            "avg_similarity":round(sum(s for s,_ in selected)/n,1) if n else 0.0,
            "top":[{"similarity":round(s,1),"symbol":str(r.get("symbol","?")),"side":str(r.get("side","?")),"return":round(row_return(r),2)} for s,r in selected[:5]]}

def pattern_signature(item):
    c=_components(item)
    ranked=sorted(((k,_f(c.get(k),50)) for k in ENGINE_KEYS if k in c),key=lambda x:abs(x[1]-50),reverse=True)
    tags=[]
    for k,v in ranked[:4]:tags.append(f"{k}:{'HIGH' if v>=60 else 'LOW' if v<=40 else 'MID'}")
    return " | ".join(tags) if tags else "NO_COMPONENT_DATA"

def quality_score(rows,completion=0.0,engine_samples=0,similarity=None):
    vals=[row_return(r) for r in rows[-300:]]
    n=len(vals); wins=sum(v>0 for v in vals)
    wr=wins/n*100 if n else 0.0
    sample=clamp(n/150*100)
    performance=clamp(.75*wr+.25*clamp(50+(sum(vals)/n if n else 0)*10))
    learning=clamp(engine_samples/80*100)
    integrity=clamp(completion)
    sim=clamp((similarity or {}).get("avg_similarity",0))
    confidence=clamp((similarity or {}).get("n",0)/12*100)
    overall=clamp(.22*sample+.24*performance+.18*learning+.16*integrity+.12*sim+.08*confidence)
    return {"overall":round(overall,1),"sample":round(sample,1),"performance":round(performance,1),
            "learning":round(learning,1),"integrity":round(integrity,1),"similarity":round(sim,1),
            "confidence":round(confidence,1),"n":n,"win_rate":round(wr,1)}

def tuning_advice(rows,min_samples=8):
    out=[]
    for k in ENGINE_KEYS:
        pairs=[]
        for r in rows:
            c=_components(r)
            if k in c:pairs.append((_f(c[k],50),row_return(r)))
        if len(pairs)<min_samples:
            out.append({"engine":k,"n":len(pairs),"action":"HOLD","delta":0.0,"edge":0.0});continue
        hi=[ret for score,ret in pairs if score>=60]; lo=[ret for score,ret in pairs if score<60]
        edge=(sum(hi)/len(hi) if hi else 0)-(sum(lo)/len(lo) if lo else 0)
        delta=round(max(-2.0,min(2.0,edge)),1)
        action="UP" if delta>=0.3 else "DOWN" if delta<=-0.3 else "HOLD"
        out.append({"engine":k,"n":len(pairs),"action":action,"delta":delta,"edge":round(edge,2)})
    return sorted(out,key=lambda x:abs(x["delta"]),reverse=True)
