"""A100 V103.0 Autonomous Evolution Engine.

Pure, network-free learning functions. This module never sends orders. It expands
outcome classification, fuzzy DNA matching, explainable false-signal filtering,
bounded self-calibration and post-outcome replay.
"""
from __future__ import annotations
import time, hashlib
from collections import defaultdict

FEATURES=("volume","oi","funding","compression","momentum","pattern","cycle","mtf")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _active(signal, threshold=50.0):
    f=signal.get("features") or {}
    return frozenset(k for k in FEATURES if _f(f.get(k))>=threshold)

def evaluate_extended_outcomes(state, prices, now=None, timeout_hours=72, reverse_signals=None, manual_exits=None, trailing_pct=0.8):
    """Close OPEN signals using TP/SL, manual, reversal, trailing or timeout rules."""
    now=_f(now,time.time()); events=[]; changed=0
    reverse_signals={str(k).upper():str(v).upper() for k,v in (reverse_signals or {}).items()}
    manual_exits={str(k):v for k,v in (manual_exits or {}).items()}
    for s in state.get("signals",[]):
        if s.get("status")!="OPEN":continue
        symbol=str(s.get("symbol") or "").upper();side=str(s.get("side") or "WAIT").upper()
        price=_f((prices or {}).get(symbol)); ref=_f(s.get("reference_price"))
        if price<=0 or ref<=0 or side not in ("LONG","SHORT"):continue
        favorable=(price/ref-1)*100*(1 if side=="LONG" else -1)
        s["best_favorable_pct"]=max(_f(s.get("best_favorable_pct")),favorable)
        result=kind=None
        manual=manual_exits.get(str(s.get("id")))
        if manual is not None:
            price=_f(manual,price);favorable=(price/ref-1)*100*(1 if side=="LONG" else -1);kind="MANUAL_EXIT"
            result="WIN" if favorable>.05 else "LOSS" if favorable<-.05 else "HOLD"
        elif reverse_signals.get(symbol) in ("LONG","SHORT") and reverse_signals[symbol]!=side:
            kind="REVERSE_SIGNAL";result="WIN" if favorable>.05 else "LOSS" if favorable<-.05 else "HOLD"
        elif (side=="LONG" and price>=_f(s.get("target2_price"))) or (side=="SHORT" and price<=_f(s.get("target2_price"))): result,kind="WIN","TP2"
        elif (side=="LONG" and price>=_f(s.get("target1_price"))) or (side=="SHORT" and price<=_f(s.get("target1_price"))): result,kind="WIN","TP1"
        elif (side=="LONG" and price<=_f(s.get("stop_price"))) or (side=="SHORT" and price>=_f(s.get("stop_price"))): result,kind="LOSS","SL"
        elif _f(s.get("best_favorable_pct"))>=max(1.0,trailing_pct*1.5) and favorable<=_f(s.get("best_favorable_pct"))-trailing_pct:
            result="WIN" if favorable>.05 else "HOLD";kind="TRAILING_EXIT"
        elif now-_f(s.get("created_at"))>=timeout_hours*3600:
            result="WIN" if favorable>.25 else "LOSS" if favorable<-.25 else "HOLD";kind="TIMEOUT"
        if result:
            s.update(status=result,closed_at=now,close_price=price,return_pct=round(favorable,6),outcome_type=kind,source="V103_AUTO_OUTCOME")
            ev={"at":now,"kind":"V103_OUTCOME","signal_id":s.get("id"),"symbol":symbol,"result":result,"outcome_type":kind,"return_pct":round(favorable,6)}
            state.setdefault("events",[]).append(ev);events.append(ev);changed+=1
    state["events"]=state.get("events",[])[-2000:]
    return {"changed":changed,"events":events}

def build_fuzzy_dna(state,min_samples=2,similarity=.60):
    """Create exact and nearby-feature DNA clusters without fabricating samples."""
    decided=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")]
    groups=[]
    for s in decided:
        aset=_active(s); chosen=None; best=0
        for g in groups:
            union=aset|g["active"]; sim=len(aset&g["active"])/len(union) if union else 1.0
            if sim>=similarity and sim>best:chosen=g;best=sim
        if chosen is None:groups.append({"active":aset,"rows":[s]})
        else:chosen["rows"].append(s)
    dna=[]
    for g in groups:
        rows=g["rows"];n=len(rows)
        if n<min_samples:continue
        wins=sum(x.get("status")=="WIN" for x in rows);wr=wins/n*100;pattern="+".join(sorted(g["active"])) or "none"
        dna.append({"id":"FDNA-"+hashlib.sha1(pattern.encode()).hexdigest()[:6].upper(),"pattern":pattern,"active":sorted(g["active"]),"n":n,"wins":wins,"losses":n-wins,"win_rate":round(wr,1),"avg_return":round(sum(_f(x.get("return_pct")) for x in rows)/n,3),"confidence":round(min(100,n/12*100),1),"status":"ELITE" if n>=5 and wr>=70 else "RISK" if n>=5 and wr<35 else "LEARNING"})
    dna.sort(key=lambda x:(-x["confidence"],-x["win_rate"],-x["n"]));state["dna_library_v103"]=dna[:120]
    return state["dna_library_v103"]

def fuzzy_dna_match(state,signal):
    aset=_active(signal);best=None;best_sim=-1
    for d in state.get("dna_library_v103",[]):
        b=set(d.get("active") or []);u=aset|b;sim=len(aset&b)/len(u) if u else 1.0
        if sim>best_sim:best,best_sim=d,sim
    if best is None:return {"id":"NEW","n":0,"win_rate":0.0,"similarity":0.0,"status":"NEW"}
    out=dict(best);out["similarity"]=round(best_sim*100,1);return out

def explain_false_signal(state,signal):
    dna=fuzzy_dna_match(state,signal);reasons=[];risk=0.0
    strategy=f"{signal.get('side','?')}|{signal.get('label','?')}"
    if strategy in set(state.get("blacklist") or []):risk+=45;reasons.append("비활성 전략과 일치")
    if dna.get("n",0)>=5 and dna.get("win_rate",100)<35:risk+=30;reasons.append("유사 DNA 저성과")
    if _f(signal.get("confidence"))<45:risk+=15;reasons.append("Confidence 부족")
    if abs(_f(signal.get("confidence"))-_f(signal.get("pump")))>25:risk+=10;reasons.append("Pump/Confidence 불일치")
    risk=min(100,risk);allow=max(0,100-risk)
    return {"risk":round(risk,1),"allow_probability":round(allow,1),"decision":"IGNORE" if risk>=60 else "CAUTION" if risk>=30 else "PASS","reasons":reasons or ["중대 약점 없음"],"dna":dna,"similar_samples":dna.get("n",0)}

def self_calibrate(state,min_samples=8,max_step=.02):
    decided=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")][-100:]
    if len(decided)<min_samples:return {"changed":False,"reason":"표본 부족","samples":len(decided),"parameters":dict(state.get("calibration_v103") or {})}
    recent=decided[-20:];wr=sum(x.get("status")=="WIN" for x in recent)/len(recent)
    old=dict(state.get("calibration_v103") or {"confidence_bias":0.0,"score_bias":0.0,"tp_multiplier":1.0,"sl_multiplier":1.0})
    direction=1 if wr>=.55 else -1 if wr<.45 else 0
    new=dict(old)
    new["confidence_bias"]=round(max(-8,min(8,_f(old.get("confidence_bias"))+direction*max_step*100)),3)
    new["score_bias"]=round(max(-8,min(8,_f(old.get("score_bias"))+direction*max_step*100)),3)
    new["tp_multiplier"]=round(max(.85,min(1.15,_f(old.get("tp_multiplier"),1)+direction*max_step)),4)
    new["sl_multiplier"]=round(max(.85,min(1.15,_f(old.get("sl_multiplier"),1)-direction*max_step/2)),4)
    state["calibration_v103"]=new
    ev={"at":time.time(),"kind":"V103_CALIBRATION","samples":len(recent),"win_rate":round(wr*100,1),"parameters":new};state.setdefault("events",[]).append(ev)
    return {"changed":new!=old,"samples":len(recent),"win_rate":round(wr*100,1),"parameters":new}

def replay_outcomes(state,limit=20):
    rows=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")][-limit:];out=[]
    for s in reversed(rows):
        f=s.get("features") or {};weak=sorted(FEATURES,key=lambda k:_f(f.get(k)))[:2];strong=sorted(FEATURES,key=lambda k:_f(f.get(k)),reverse=True)[:2]
        causes=[]
        if s.get("status")=="LOSS":
            causes=[f"{k} 근거 부족" for k in weak]
            if _f(s.get("confidence"))>=70:causes.append("과도한 Confidence")
        else:causes=[f"{k} 강점 기여" for k in strong]
        out.append({"signal_id":s.get("id"),"symbol":s.get("symbol"),"side":s.get("side"),"result":s.get("status"),"outcome_type":s.get("outcome_type","MATCHED"),"return_pct":_f(s.get("return_pct")),"causes":causes[:3]})
    state["replays_v103"]=out
    return out

def growth_summary(state,limit=30):
    rows=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")][-limit:];curve=[];wins=0
    for i,s in enumerate(rows,1):wins+=s.get("status")=="WIN";curve.append(round(wins/i*100,1))
    return {"samples":len(rows),"win_rate":curve[-1] if curve else 0.0,"curve":curve,"dna":len(state.get("dna_library_v103",[])),"replays":len(state.get("replays_v103",[])),"calibration":dict(state.get("calibration_v103") or {})}
