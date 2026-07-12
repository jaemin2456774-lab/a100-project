"""A100 V96.2 AI Intelligence 3 analytics.
Safe, deterministic analytics only: no network calls, order execution, or state mutation.
Schema-1 compatible and tolerant of sparse historical rows.
"""
from __future__ import annotations
from datetime import datetime, timezone
from math import sqrt


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d


def clamp(v, lo=0.0, hi=100.0): return max(lo, min(hi, _f(v)))


def row_return(row):
    for k in ("realized_pct", "return_pct", "pnl_pct", "result_pct"):
        if k in row: return _f(row.get(k))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p


def _ts(row):
    for k in ("closed_at", "exit_time", "timestamp", "time", "created_at", "opened_at"):
        v=row.get(k)
        if v is None: continue
        try:
            if isinstance(v,(int,float)):
                x=float(v); x=x/1000 if x>10_000_000_000 else x
                return datetime.fromtimestamp(x, tz=timezone.utc).timestamp()
            s=str(v).strip().replace("Z", "+00:00")
            dt=datetime.fromisoformat(s)
            if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except Exception: pass
    return None


def calibration_report(rows, bins=5):
    """Compare stated confidence with observed outcomes and return safe correction advice."""
    samples=[]
    for r in rows:
        conf=None
        for k in ("confidence", "ai_confidence", "decision_confidence", "score"):
            if r.get(k) is not None: conf=clamp(r.get(k)); break
        if conf is None: continue
        samples.append((conf, 100.0 if row_return(r)>0 else 0.0))
    if not samples:
        return {"n":0,"predicted":0.0,"actual":0.0,"error":0.0,"mae":0.0,"status":"표본 부족","adjustment":0.0,"bins":[]}
    predicted=sum(x for x,_ in samples)/len(samples); actual=sum(y for _,y in samples)/len(samples)
    error=actual-predicted; mae=sum(abs(y-x) for x,y in samples)/len(samples)
    adjustment=max(-8.0,min(8.0,error*0.25))
    out=[]
    width=100/bins
    for i in range(bins):
        lo=i*width; hi=(i+1)*width
        vals=[(x,y) for x,y in samples if lo<=x<(hi if i<bins-1 else hi+0.001)]
        if vals: out.append({"range":f"{int(lo)}-{int(hi)}","n":len(vals),"predicted":round(sum(x for x,_ in vals)/len(vals),1),"actual":round(sum(y for _,y in vals)/len(vals),1)})
    status="양호" if abs(error)<=8 and mae<=38 else "과신" if error<0 else "보수적"
    return {"n":len(samples),"predicted":round(predicted,1),"actual":round(actual,1),"error":round(error,1),"mae":round(mae,1),"status":status,"adjustment":round(adjustment,1),"bins":out}


def memory_windows(rows, now_ts=None):
    now_ts=_f(now_ts, datetime.now(timezone.utc).timestamp())
    specs=(("1D",86400),("7D",7*86400),("30D",30*86400),("ALL",None)); out={}
    timestamped=[r for r in rows if _ts(r) is not None]
    for name,sec in specs:
        selected=list(rows) if sec is None else ([r for r in timestamped if now_ts-_ts(r)<=sec] if timestamped else list(rows)[-min(len(rows), {"1D":24,"7D":100,"30D":300}[name]):])
        vals=[row_return(r) for r in selected]; n=len(vals); wins=sum(v>0 for v in vals)
        out[name]={"n":n,"win_rate":round(wins/n*100,1) if n else 0.0,"avg":round(sum(vals)/n,2) if n else 0.0}
    return out


def rank_candidate(item, sim, quality=0.0, calibration=None):
    calibration=calibration or {}
    wr=_f(sim.get("win_rate")); similarity=_f(sim.get("avg_similarity")); avg=_f(sim.get("weighted_return",sim.get("avg",0)))
    n=int(sim.get("n",0)); conf=clamp(item.get("confidence",item.get("score",50)))
    correction=_f(calibration.get("adjustment")); calibrated=clamp(conf+correction)
    evidence=clamp(n/20*100); expected=clamp(50+avg*8)
    risk=clamp(100-_f((item.get("components") or {}).get("Risk",50)))
    total=clamp(.24*wr+.18*similarity+.18*_f(quality)+.16*calibrated+.14*evidence+.10*expected-.08*risk)
    grade="A+" if total>=82 else "A" if total>=74 else "B" if total>=64 else "C" if total>=54 else "D"
    action="PAPER" if total>=72 and n>=5 and avg>0 else "WATCH" if total>=58 else "AVOID"
    return {"symbol":str(item.get("symbol","?")),"side":str(item.get("side","WAIT")),"score":round(total,1),"grade":grade,"action":action,"calibrated_confidence":round(calibrated,1),"evidence":round(evidence,1),"expected":round(expected,1),"risk":round(risk,1),"n":n}


def shadow_replay(rows):
    shadow=[r for r in rows if str(r.get("mode") or r.get("source") or r.get("trade_type") or "").lower() in {"shadow","paper_shadow","shadow_trade"} or bool(r.get("shadow"))]
    if not shadow: shadow=list(rows)
    vals=[row_return(r) for r in shadow]; n=len(vals); wins=sum(v>0 for v in vals)
    missed=[v for v in vals if v>0]; avoided=[v for v in vals if v<0]
    return {"n":n,"win_rate":round(wins/n*100,1) if n else 0.0,"avg":round(sum(vals)/n,2) if n else 0.0,
            "missed_opportunity":round(sum(missed),2),"avoided_loss":round(abs(sum(avoided)),2),
            "best":round(max(vals),2) if vals else 0.0,"worst":round(min(vals),2) if vals else 0.0}


def health_report(rows, quality=0.0, command_sync=True):
    mem=memory_windows(rows); cal=calibration_report(rows); shadow=shadow_replay(rows)
    sample=clamp(mem["ALL"]["n"]/300*100); consistency=clamp(100-abs(mem["7D"]["win_rate"]-mem["30D"]["win_rate"])*2)
    calibration=clamp(100-abs(cal.get("error",0))*2-cal.get("mae",0)*.35)
    shadow_score=clamp(shadow["n"]/100*100)
    integrity=100.0 if command_sync else 40.0
    overall=clamp(.25*_f(quality)+.20*sample+.20*calibration+.15*consistency+.10*shadow_score+.10*integrity)
    status="정상" if overall>=75 else "학습 중" if overall>=55 else "점검 필요"
    return {"overall":round(overall,1),"status":status,"sample":round(sample,1),"calibration":round(calibration,1),"consistency":round(consistency,1),"shadow":round(shadow_score,1),"integrity":round(integrity,1),"memory":mem,"calibration_detail":cal,"shadow_detail":shadow}
