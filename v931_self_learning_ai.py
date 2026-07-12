"""A100 V93.1 Self-Learning AI.
Pure analytics over existing schema-1 closed Paper/Shadow rows.
No network, state mutation, scheduler, or live-order path.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from math import sqrt

ENGINE_KEYS=("Pattern","Liquidity","Momentum","Market","Risk","Timing","Learning","Meta")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def row_return(row):
    if "realized_pct" in row:return _f(row.get("realized_pct"))
    for k in ("return_pct","pnl_pct","result_pct"):
        if k in row:return _f(row.get(k))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p

def wilson(wins,n,z=1.96):
    if n<=0:return (0.0,100.0)
    p=wins/n; den=1+z*z/n
    mid=(p+z*z/(2*n))/den
    half=z*sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return (max(0,(mid-half)*100),min(100,(mid+half)*100))

def calibrated_probability(raw_confidence, rows):
    vals=[row_return(r) for r in rows]
    n=len(vals); wins=sum(v>0 for v in vals)
    empirical=wins/n*100 if n else 50.0
    # Bayesian shrinkage: 20 neutral pseudo-observations; confidence has limited influence.
    calibrated=(wins+10)/(n+20)*100 if n else 50.0
    calibrated=0.75*calibrated+0.25*max(1,min(99,_f(raw_confidence,50)))
    lo,hi=wilson(wins,n)
    return {"n":n,"wins":wins,"empirical":round(empirical,1),"probability":round(calibrated,1),"ci_low":round(lo,1),"ci_high":round(hi,1)}

def _regime(row):
    x=row.get("regime_at_entry",row.get("regime","UNKNOWN"))
    if isinstance(x,dict):x=x.get("regime",x.get("name","UNKNOWN"))
    return str(x or "UNKNOWN").upper()

def grouped_memory(rows):
    groups={"side":defaultdict(list),"regime":defaultdict(list),"symbol":defaultdict(list),"sample":defaultdict(list)}
    for r in rows:
        ret=row_return(r)
        groups["side"][str(r.get("side","UNKNOWN")).upper()].append(ret)
        groups["regime"][_regime(r)].append(ret)
        groups["symbol"][str(r.get("symbol","UNKNOWN")).upper()].append(ret)
        groups["sample"][str(r.get("sample_type","UNKNOWN")).upper()].append(ret)
    out={}
    for kind,buckets in groups.items():
        stats=[]
        for key,vals in buckets.items():
            n=len(vals); wins=sum(v>0 for v in vals)
            stats.append({"key":key,"n":n,"win_rate":round(wins/n*100,1) if n else 0.0,"avg":round(sum(vals)/n,2) if n else 0.0})
        out[kind]=sorted(stats,key=lambda x:(x["n"],x["win_rate"]),reverse=True)
    return out

def learned_engine_multipliers(rows,min_samples=8):
    buckets={k:[] for k in ENGINE_KEYS}
    for r in rows:
        comps=r.get("components") or r.get("engine_scores") or r.get("scores") or {}
        if not isinstance(comps,dict):continue
        ret=row_return(r)
        for k in ENGINE_KEYS:
            if k in comps:buckets[k].append((_f(comps[k],50),ret))
    result={}
    for k,pairs in buckets.items():
        n=len(pairs)
        if n<min_samples:
            result[k]={"n":n,"multiplier":1.0,"edge":0.0}
            continue
        hi=[ret for score,ret in pairs if score>=60]; lo=[ret for score,ret in pairs if score<60]
        hi_avg=sum(hi)/len(hi) if hi else 0; lo_avg=sum(lo)/len(lo) if lo else 0
        edge=max(-2.0,min(2.0,hi_avg-lo_avg))
        result[k]={"n":n,"multiplier":round(max(.75,min(1.25,1+edge*.10)),3),"edge":round(edge,3)}
    return result

def apply_learning(base_weights,rows):
    learned=learned_engine_multipliers(rows)
    raw={k:_f(v)*learned.get(k,{"multiplier":1})["multiplier"] for k,v in base_weights.items()}
    total=sum(raw.values()) or 1
    return ({k:round(v/total*100,1) for k,v in raw.items()},learned)

def explain(symbol,side,verdict,regime,contributions,calibration,similar=None):
    pos=[x for x in contributions if x.get("contribution",0)>.5][:3]
    neg=[x for x in contributions if x.get("contribution",0)<-.5][:3]
    parts=[]
    if pos:parts.append("지지: "+", ".join(x["engine"] for x in pos))
    if neg:parts.append("억제: "+", ".join(x["engine"] for x in neg))
    if not parts:parts.append("뚜렷한 엔진 우위 부족")
    sim=""
    if similar and similar.get("n",0):sim=f" 유사 표본 {similar['n']}건 승률 {similar['win_rate']:.1f}%."
    return f"{symbol} {side}: {' / '.join(parts)}. 시장 국면 {regime}, 최종 {verdict}. 보정 예상승률 {calibration['probability']:.1f}% (95% 범위 {calibration['ci_low']:.1f}~{calibration['ci_high']:.1f}%).{sim}"

def similar_stats(rows,symbol,side,regime):
    levels=[
      [r for r in rows if str(r.get('symbol','')).upper()==symbol and str(r.get('side','')).upper()==side and _regime(r)==regime],
      [r for r in rows if str(r.get('symbol','')).upper()==symbol and str(r.get('side','')).upper()==side],
      [r for r in rows if str(r.get('side','')).upper()==side and _regime(r)==regime],
      [r for r in rows if str(r.get('side','')).upper()==side],
    ]
    sample=next((x for x in levels if len(x)>=5),levels[-1])
    vals=[row_return(r) for r in sample]; n=len(vals); wins=sum(v>0 for v in vals)
    return {"n":n,"win_rate":wins/n*100 if n else 0.0,"avg":sum(vals)/n if n else 0.0}
