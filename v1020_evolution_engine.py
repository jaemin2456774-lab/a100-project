"""A100 V102.0 Evolution Engine.

Network-free learning primitives. Callers provide current prices; this module never
fetches market data and never places/modifies orders.
"""
from __future__ import annotations
import time, hashlib
from collections import defaultdict

FEATURES=("volume","oi","funding","compression","momentum","pattern","cycle","mtf")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def attach_reference(signal, price, now=None):
    p=_f(price)
    if p<=0:return False
    signal.setdefault("reference_price",p)
    signal.setdefault("reference_at",_f(now,time.time()))
    plan=signal.get("entry_plan") or {}; side=str(signal.get("side") or "WAIT").upper()
    stop=abs(_f(plan.get("stop_pct"),1.2))/100
    t1=abs(_f(plan.get("target1_pct"),1.5))/100
    t2=abs(_f(plan.get("target2_pct"),2.2))/100
    if side=="LONG":
        signal.setdefault("stop_price",p*(1-stop));signal.setdefault("target1_price",p*(1+t1));signal.setdefault("target2_price",p*(1+t2))
    elif side=="SHORT":
        signal.setdefault("stop_price",p*(1+stop));signal.setdefault("target1_price",p*(1-t1));signal.setdefault("target2_price",p*(1-t2))
    return True

def evaluate_open_signals(state, prices, now=None, timeout_hours=72):
    now=_f(now,time.time()); changed=0; events=[]
    for s in state.get("signals",[]):
        if s.get("status")!="OPEN":continue
        symbol=str(s.get("symbol") or "").upper(); price=_f((prices or {}).get(symbol))
        if price<=0:continue
        if not s.get("reference_price"):attach_reference(s,price,now)
        ref=_f(s.get("reference_price")); side=str(s.get("side") or "WAIT").upper()
        if ref<=0 or side not in ("LONG","SHORT"):continue
        s["last_price"]=price;s["last_observed_at"]=now
        favorable=(price/ref-1)*100*(1 if side=="LONG" else -1)
        adverse=-favorable
        result=None; milestone=None
        if (side=="LONG" and price>=_f(s.get("target2_price"))) or (side=="SHORT" and price<=_f(s.get("target2_price"))): result="WIN";milestone="TP2"
        elif (side=="LONG" and price>=_f(s.get("target1_price"))) or (side=="SHORT" and price<=_f(s.get("target1_price"))): result="WIN";milestone="TP1"
        elif (side=="LONG" and price<=_f(s.get("stop_price"))) or (side=="SHORT" and price>=_f(s.get("stop_price"))): result="LOSS";milestone="SL"
        elif now-_f(s.get("created_at"))>=timeout_hours*3600: result="HOLD";milestone="TIMEOUT"
        if result:
            s.update({"status":result,"closed_at":now,"close_price":price,"return_pct":round(favorable,6),"outcome_type":milestone,"source":"LIVE_OBSERVATION"})
            ev={"at":now,"kind":"LIVE_OUTCOME","signal_id":s.get("id"),"result":result,"outcome_type":milestone,"return_pct":round(favorable,6)}
            state.setdefault("events",[]).append(ev);events.append(ev);changed+=1
    state["events"]=state.get("events",[])[-2000:]
    return {"changed":changed,"events":events}

def adaptive_learn(state,min_samples=3,max_step=.025):
    decided=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")]
    weights=dict(state.get("weights") or {k:1.0 for k in FEATURES}); stats={}
    for k in FEATURES:
        active=[s for s in decided if _f((s.get("features") or {}).get(k))>=50]
        wins=sum(s.get("status")=="WIN" for s in active);n=len(active);wr=wins/n if n else .5
        if n>=min_samples:
            confidence=min(1.0,n/20);delta=max(-max_step,min(max_step,(wr-.5)*2*max_step*confidence))
            weights[k]=round(max(.50,min(1.50,_f(weights.get(k),1)+delta)),4)
        stats[k]={"n":n,"wins":wins,"win_rate":round(wr*100,1) if n else 0.0,"weight":weights.get(k,1.0)}
    state["weights"]=weights;state["feature_stats"]=stats
    return stats

def _dna_key(signal):
    f=signal.get("features") or {}; active=sorted(k for k in FEATURES if _f(f.get(k))>=50)
    return "+".join(active) or "none"

def build_dna(state,min_samples=2):
    groups=defaultdict(list)
    for s in state.get("signals",[]):
        if s.get("status") in ("WIN","LOSS"):groups[_dna_key(s)].append(s)
    dna=[]
    for key,rows in groups.items():
        n=len(rows);wins=sum(x.get("status")=="WIN" for x in rows);wr=wins/n*100
        if n>=min_samples:
            dna.append({"id":"DNA-"+hashlib.sha1(key.encode()).hexdigest()[:6].upper(),"pattern":key,"n":n,"wins":wins,"win_rate":round(wr,1),"avg_return":round(sum(_f(x.get('return_pct')) for x in rows)/n,3),"status":"ELITE" if n>=5 and wr>=70 else "WEAK" if n>=5 and wr<35 else "LEARNING"})
    dna.sort(key=lambda x:(-x["win_rate"],-x["n"]));state["dna_library"]=dna[:100]
    return state["dna_library"]

def dna_match(state, signal):
    key=_dna_key(signal)
    for d in state.get("dna_library",[]):
        if d.get("pattern")==key:return d
    return {"id":"NEW","pattern":key,"n":0,"win_rate":0.0,"status":"NEW"}

def false_signal_risk(state, signal):
    reasons=[];score=0.0
    strategy=f"{signal.get('side','?')}|{signal.get('label','?')}"
    if strategy in set(state.get("blacklist") or []):score+=55;reasons.append("블랙리스트 전략")
    dna=dna_match(state,signal)
    if dna.get("n",0)>=5 and dna.get("win_rate",100)<35:score+=30;reasons.append("저성과 DNA")
    conf=_f(signal.get("confidence"));pump=_f(signal.get("pump"))
    if conf<45:score+=15;reasons.append("낮은 Confidence")
    if abs(conf-pump)>25:score+=10;reasons.append("Pump/Confidence 불일치")
    risk=min(100,score);return {"risk":risk,"decision":"IGNORE" if risk>=60 else "CAUTION" if risk>=30 else "PASS","reasons":reasons or ["중대 약점 없음"],"dna":dna}

def confidence_evolution(state,limit=20):
    rows=[s for s in state.get("signals",[]) if s.get("status") in ("WIN","LOSS")][-limit:]
    trend=[];correct=0
    for i,s in enumerate(rows,1):
        correct+=1 if s.get("status")=="WIN" else 0
        trend.append(round(correct/i*100,1))
    recent=trend[-1] if trend else 0.0
    return {"n":len(rows),"trend":trend,"recent_accuracy":recent,"direction":"UP" if len(trend)>=4 and trend[-1]>trend[max(0,len(trend)-4)] else "DOWN" if len(trend)>=4 and trend[-1]<trend[max(0,len(trend)-4)] else "STABLE"}

def dynamic_score(base_score,state,signal):
    evo=confidence_evolution(state);dna=dna_match(state,signal);fs=false_signal_risk(state,signal)
    performance=(evo["recent_accuracy"]-50)*.12 if evo["n"]>=3 else 0
    dna_adj=(dna.get("win_rate",50)-50)*.08 if dna.get("n",0)>=2 else 0
    penalty=fs["risk"]*.15
    score=max(0,min(100,_f(base_score)+performance+dna_adj-penalty))
    return {"score":round(score,1),"base":round(_f(base_score),1),"performance_adj":round(performance,1),"dna_adj":round(dna_adj,1),"false_penalty":round(penalty,1),"false":fs,"evolution":evo,"dna":dna}
