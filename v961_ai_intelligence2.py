"""A100 V96.1 AI Intelligence 2 analytics.
Pure deterministic analytics. No network calls, no state mutation, no live execution.
Schema-1 compatible and tolerant of sparse historical rows.
"""
from __future__ import annotations
from math import sqrt

ENGINE_KEYS=("Pattern","Liquidity","Momentum","Market","Risk","Timing","Learning","Meta")
SCALAR_KEYS=("score","confidence","funding","funding_rate","oi_change","open_interest_change","volume_change","change_24h","spread")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def clamp(v,lo=0.0,hi=100.0): return max(lo,min(hi,_f(v)))

def components(obj):
    c=obj.get("components") or obj.get("engine_scores") or obj.get("scores") or {}
    return c if isinstance(c,dict) else {}

def row_return(row):
    for k in ("realized_pct","return_pct","pnl_pct","result_pct"):
        if k in row:return _f(row.get(k))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p

def _norm_scalar(k,v):
    v=_f(v)
    if k in ("score","confidence"): return clamp(v)
    if "funding" in k: return clamp(50+v*5000)
    if "spread" in k: return clamp(100-v*1000)
    return clamp(50+v*5)

def feature_vector(obj):
    c=components(obj); out={}
    for k in ENGINE_KEYS:
        if k in c: out["E:"+k]=clamp(c[k])
    for k in SCALAR_KEYS:
        if k in obj and obj.get(k) is not None: out["S:"+k]=_norm_scalar(k,obj.get(k))
    regime=str(obj.get("regime") or obj.get("market_regime") or "").upper()
    if regime: out["R:"+regime]=100.0
    return out

def vector_similarity(a,b):
    va=feature_vector(a); vb=feature_vector(b)
    common=[k for k in va if k in vb]
    if not common:return 0.0
    # Root mean square distance, with a small coverage reward.
    dist=sqrt(sum((va[k]-vb[k])**2 for k in common)/len(common))
    coverage=min(1.0,len(common)/8.0)
    return round(clamp((100-dist*1.7)*(0.72+0.28*coverage)),1)

def find_similar_v2(item,rows,limit=20,min_score=38.0):
    symbol=str(item.get("symbol","")).upper(); side=str(item.get("side","")).upper()
    regime=str(item.get("regime") or item.get("market_regime") or "").upper()
    ranked=[]
    for r in rows:
        base=vector_similarity(item,r)
        rs=str(r.get("symbol","")).upper(); rd=str(r.get("side","")).upper()
        rr=str(r.get("regime") or r.get("market_regime") or "").upper()
        # Sparse-data fallback still permits learning without fabricating component similarity.
        if base<=0:
            base=18.0 + (14.0 if rs==symbol else 0.0) + (12.0 if rd==side else 0.0) + (8.0 if regime and rr==regime else 0.0)
        total=base+(7 if rs==symbol else 0)+(6 if rd==side else 0)+(5 if regime and rr==regime else 0)
        total=clamp(total)
        if total>=min_score: ranked.append((total,r))
    ranked.sort(key=lambda x:x[0],reverse=True)
    selected=ranked[:max(1,int(limit))]
    vals=[row_return(r) for _,r in selected]; n=len(vals); wins=sum(v>0 for v in vals)
    weighted_den=sum(s for s,_ in selected)
    weighted=sum(s*row_return(r) for s,r in selected)/weighted_den if weighted_den else 0.0
    return {"n":n,"win_rate":round(wins/n*100,1) if n else 0.0,"avg":round(sum(vals)/n,2) if n else 0.0,
            "weighted_return":round(weighted,2),"avg_similarity":round(sum(s for s,_ in selected)/n,1) if n else 0.0,
            "top":[{"similarity":round(s,1),"symbol":str(r.get("symbol","?")),"side":str(r.get("side","?")),
                    "return":round(row_return(r),2),"regime":str(r.get("regime") or r.get("market_regime") or "-")} for s,r in selected[:5]]}

def bucket(v):
    v=_f(v,50)
    return "H" if v>=65 else "L" if v<=35 else "M"

def pattern_signature_v2(item):
    c=components(item); sym=str(item.get("symbol","?")).upper(); side=str(item.get("side","?")).upper()
    regime=str(item.get("regime") or item.get("market_regime") or "UNKNOWN").upper()
    parts=[sym,side,regime]
    for k in ENGINE_KEYS:
        if k in c:parts.append(f"{k[:3]}:{bucket(c[k])}")
    return "|".join(parts)

def explain(item,sim):
    c=components(item); reasons=[]
    ranked=sorted(c.items(),key=lambda kv:abs(_f(kv[1])-50),reverse=True)
    for k,v in ranked[:4]:
        v=_f(v); reasons.append(f"{k} {'지지' if v>=60 else '억제' if v<=40 else '중립'} ({v:.0f})")
    if sim.get("n",0): reasons.append(f"유사 {sim['n']}건 승률 {sim['win_rate']:.1f}%")
    regime=str(item.get("regime") or item.get("market_regime") or "UNKNOWN").upper()
    reasons.append(f"시장 국면 {regime}")
    return reasons

def recommendation(item,sim,quality=0.0):
    side=str(item.get("side","WAIT")).upper(); wr=_f(sim.get("win_rate")); n=int(sim.get("n",0)); avg=_f(sim.get("weighted_return"))
    evidence=clamp(n/20*100); confidence=clamp(.45*wr+.25*quality+.20*sim.get("avg_similarity",0)+.10*evidence)
    if n<5 or confidence<52:return {"action":"AVOID","side":side,"confidence":round(confidence,1),"stars":max(1,min(5,round(confidence/20)))}
    if wr>=58 and avg>0:return {"action":"WATCH" if confidence<68 else "PAPER", "side":side,"confidence":round(confidence,1),"stars":max(1,min(5,round(confidence/20)))}
    return {"action":"AVOID","side":side,"confidence":round(confidence,1),"stars":max(1,min(5,round(confidence/20)))}

def replay_steps(item,sim,quality):
    rec=recommendation(item,sim,quality)
    return [
      ("1. Feature",f"엔진/시장 특징 {len(feature_vector(item))}개 정규화"),
      ("2. Similarity",f"과거 {sim.get('n',0)}건 · 평균 유사 {sim.get('avg_similarity',0):.1f}%"),
      ("3. Outcome",f"유사 승률 {sim.get('win_rate',0):.1f}% · 가중수익 {sim.get('weighted_return',0):+.2f}%"),
      ("4. Quality",f"AI 품질 {quality:.1f}%"),
      ("5. Decision",f"{rec['action']} {rec['side']} · 신뢰 {rec['confidence']:.1f}%")]
