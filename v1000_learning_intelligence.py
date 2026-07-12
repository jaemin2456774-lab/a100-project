"""A100 V100.0 Learning Intelligence.
Deterministic, schema-1 compatible analytics. No network calls, no order execution,
and no state mutation. It evaluates true time windows, decay-weighted outcomes,
confidence calibration, and score contribution transparency.
"""
from __future__ import annotations
from datetime import datetime, timezone
from math import exp


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d


def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, _f(v)))


def row_return(row):
    for k in ("realized_pct", "return_pct", "pnl_pct", "result_pct"):
        if row.get(k) is not None: return _f(row.get(k))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p


def row_ts(row):
    for k in ("closed_at", "exit_time", "timestamp", "time", "created_at", "opened_at"):
        v=row.get(k)
        if v is None: continue
        try:
            if isinstance(v,(int,float)):
                x=float(v); x=x/1000 if x>10_000_000_000 else x
                return x
            dt=datetime.fromisoformat(str(v).strip().replace("Z","+00:00"))
            if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except Exception: pass
    return None


def true_memory(rows, now_ts=None):
    """Strict timestamp windows. Untimestamped rows belong only to ALL."""
    now=_f(now_ts, datetime.now(timezone.utc).timestamp())
    specs=(('1D',86400),('7D',604800),('30D',2592000))
    out={}
    for name,seconds in specs:
        selected=[r for r in rows if row_ts(r) is not None and 0 <= now-row_ts(r) <= seconds]
        vals=[row_return(r) for r in selected]
        out[name]=_stats(vals, len(selected), timestamped=len(selected))
    vals=[row_return(r) for r in rows]
    tsn=sum(row_ts(r) is not None for r in rows)
    out['ALL']=_stats(vals,len(rows),timestamped=tsn)
    out['coverage_pct']=round(tsn/len(rows)*100,1) if rows else 0.0
    return out


def _stats(vals,n,timestamped=0):
    wins=sum(v>0.05 for v in vals); losses=sum(v<-.05 for v in vals); holds=n-wins-losses
    decided=wins+losses
    return {'n':n,'wins':wins,'losses':losses,'holds':holds,
            'win_rate':round(wins/decided*100,1) if decided else 0.0,
            'avg':round(sum(vals)/n,3) if n else 0.0,'timestamped':timestamped}


def decay_learning(rows, now_ts=None, half_life_days=14.0):
    now=_f(now_ts, datetime.now(timezone.utc).timestamp()); weighted=[]
    for r in rows:
        ts=row_ts(r)
        age_days=max(0.0,(now-ts)/86400) if ts is not None else half_life_days*2
        w=exp(-0.69314718056*age_days/max(.1,half_life_days))
        ret=row_return(r); conf=clamp(r.get('confidence',r.get('ai_confidence',r.get('score',50))))
        weighted.append((ret,conf,w,age_days))
    sw=sum(x[2] for x in weighted)
    wr=sum((1 if x[0]>.05 else 0)*x[2] for x in weighted)/sw*100 if sw else 0
    avg=sum(x[0]*x[2] for x in weighted)/sw if sw else 0
    effective=sum(x[2] for x in weighted)
    freshness=sum((100 if x[3]<=7 else 65 if x[3]<=30 else 25)*x[2] for x in weighted)/sw if sw else 0
    return {'n':len(weighted),'weighted_win_rate':round(wr,1),'weighted_avg':round(avg,3),
            'effective_sample':round(effective,1),'freshness':round(freshness,1),'half_life_days':half_life_days}


def validation_loop(rows):
    evaluated=[]
    for r in rows:
        ret=row_return(r)
        conf=clamp(r.get('confidence',r.get('ai_confidence',r.get('decision_confidence',r.get('score',50)))))
        if abs(ret)<=.05: continue
        actual=100.0 if ret>0 else 0.0
        evaluated.append((conf,actual,ret))
    n=len(evaluated)
    if not n:return {'n':0,'wins':0,'losses':0,'win_rate':0.0,'brier':0.0,'bias':0.0,'reliability':0.0,'status':'표본 부족','suggested_shift':0.0}
    wins=sum(a==100 for _,a,_ in evaluated); pred=sum(c for c,_,_ in evaluated)/n; actual=wins/n*100
    brier=sum(((c/100)-(a/100))**2 for c,a,_ in evaluated)/n*100
    bias=actual-pred; reliability=clamp(100-brier-abs(bias)*.6)
    status='양호' if reliability>=70 else '보정 필요' if reliability>=45 else '재학습 필요'
    return {'n':n,'wins':wins,'losses':n-wins,'win_rate':round(actual,1),'brier':round(brier,1),
            'bias':round(bias,1),'reliability':round(reliability,1),'status':status,
            'suggested_shift':round(max(-10,min(10,bias*.2)),1)}


def score_breakdown(candidate, cycle, health, evolution, calibration, shadow):
    risk=_f((candidate.get('signals') or {}).get('risk'),50)
    cal=clamp(100-abs(_f(calibration.get('error')))*2-_f(calibration.get('mae'))*.25)
    sh=clamp(.72*_f(shadow.get('win_rate'))+.28*min(100,_f(shadow.get('n'))*2))
    components=[
      ('Pump',.28*_f(candidate.get('probability_v2',candidate.get('probability')))),
      ('Confidence',.20*_f(candidate.get('confidence'))),('Cycle',.13*_f(cycle.get('confidence'))),
      ('Health',.12*_f(health.get('overall'))),('Learning',.12*_f(evolution.get('composite'))),
      ('Calibration',.08*cal),('Shadow',.07*sh),('Risk',-.10*risk)]
    total=clamp(sum(v for _,v in components))
    return {'score':round(total,1),'components':[{'name':n,'points':round(v,1)} for n,v in components],
            'positive':round(sum(max(0,v) for _,v in components),1),'penalty':round(sum(min(0,v) for _,v in components),1)}


def learning_readiness(memory, decay, validation):
    coverage=_f(memory.get('coverage_pct')); sample=clamp(_f(memory.get('ALL',{}).get('n'))/200*100)
    score=clamp(.30*coverage+.25*sample+.25*_f(validation.get('reliability'))+.20*_f(decay.get('freshness')))
    grade='A+' if score>=88 else 'A' if score>=78 else 'B' if score>=66 else 'C' if score>=54 else 'D'
    return {'score':round(score,1),'grade':grade,'status':'READY' if score>=75 else 'LEARNING' if score>=50 else 'DATA_NEEDED'}
