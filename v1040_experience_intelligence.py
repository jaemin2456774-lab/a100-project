"""A100 V104.0 Experience Intelligence Engine.

Network-free, order-free learning utilities. Builds an auditable experience bank,
transfers evidence across related symbols, merges DNA, evaluates multi-horizon
memory, forecasts confidence, explains feature contribution, and proposes only
bounded recommendation parameters. It never places or modifies live orders.
"""
from __future__ import annotations
import time, hashlib
from collections import defaultdict

FEATURES=("volume","oi","funding","compression","momentum","pattern","cycle","mtf")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _features(signal):
    raw=signal.get("features") or signal.get("signals") or {}
    return {k:round(_f(raw.get(k)),4) for k in FEATURES}

def capture_experiences(state, max_rows=5000):
    """Idempotently convert decided signals into immutable experience rows."""
    bank=list(state.get("experience_bank_v104") or []); seen={x.get("signal_id") for x in bank}
    added=0
    for s in state.get("signals",[]):
        if s.get("status") not in ("WIN","LOSS","HOLD") or s.get("id") in seen:continue
        f=_features(s); symbol=str(s.get("symbol") or "").upper()
        row={"id":"EXP-"+hashlib.sha1(str(s.get("id")).encode()).hexdigest()[:10].upper(),"signal_id":s.get("id"),
             "symbol":symbol,"base":symbol.replace("USDT","").replace("BUSD",""),"side":str(s.get("side") or "WAIT").upper(),
             "result":s.get("status"),"return_pct":round(_f(s.get("return_pct")),6),"outcome_type":s.get("outcome_type","MATCHED"),
             "confidence":round(_f(s.get("confidence")),3),"score":round(_f(s.get("score",s.get("pump"))),3),
             "features":f,"created_at":_f(s.get("created_at")),"closed_at":_f(s.get("closed_at"),time.time()),"source":"V104_EXPERIENCE"}
        bank.append(row);seen.add(s.get("id"));added+=1
    bank.sort(key=lambda x:(x.get("closed_at",0),x.get("id","")))
    state["experience_bank_v104"]=bank[-max_rows:]
    return {"added":added,"total":len(state["experience_bank_v104"])}

def _similarity(a,b):
    # normalized feature distance + direction compatibility
    fa=a.get("features") or {};fb=b.get("features") or {}
    dist=sum(abs(_f(fa.get(k))-_f(fb.get(k))) for k in FEATURES)/(100*len(FEATURES))
    sim=max(0.0,1.0-dist)
    if a.get("side") and b.get("side") and a.get("side")!=b.get("side"):sim*=.72
    return sim

def cross_coin_learning(state, signal, min_similarity=.68, limit=50):
    """Transfer only weighted evidence; never copy outcomes or fabricate samples."""
    q={"features":_features(signal),"side":str(signal.get("side") or "WAIT").upper(),"symbol":str(signal.get("symbol") or "").upper()}
    rows=[]
    for x in state.get("experience_bank_v104",[]):
        if x.get("symbol")==q["symbol"]:continue
        sim=_similarity(q,x)
        if sim>=min_similarity: rows.append((sim,x))
    rows=sorted(rows,key=lambda z:(-z[0],-z[1].get("closed_at",0)))[:limit]
    weight=sum(s for s,_ in rows); wins=sum(s for s,x in rows if x.get("result")=="WIN")
    wr=wins/weight*100 if weight else 0.0
    symbols=defaultdict(int)
    for _,x in rows:symbols[x.get("symbol","?")]+=1
    return {"samples":len(rows),"weighted_win_rate":round(wr,1),"avg_similarity":round(sum(s for s,_ in rows)/len(rows)*100,1) if rows else 0.0,
            "source_symbols":dict(sorted(symbols.items(),key=lambda z:-z[1])[:8]),"confidence_adjustment":round(max(-8,min(8,(wr-50)*.16)) if len(rows)>=3 else 0.0,2)}

def build_master_dna(state,min_samples=3):
    """Merge V103 DNA into stable feature-signature master groups."""
    groups=defaultdict(list)
    for d in state.get("dna_library_v103",[]):
        active=tuple(sorted(d.get("active") or [])); key=active[:4] if active else ("none",)
        groups[key].append(d)
    out=[]
    for key,rows in groups.items():
        n=sum(int(x.get("n",0)) for x in rows)
        if n<min_samples:continue
        wins=sum(_f(x.get("win_rate"))*int(x.get("n",0))/100 for x in rows);wr=wins/n*100 if n else 0
        out.append({"id":"MDNA-"+hashlib.sha1("+".join(key).encode()).hexdigest()[:7].upper(),"signature":"+".join(key),"members":len(rows),"samples":n,
                    "win_rate":round(wr,1),"confidence":round(min(100,n/20*100),1),"status":"MASTER" if n>=10 else "FORMING"})
    out.sort(key=lambda x:(-x["samples"],-x["win_rate"]));state["master_dna_v104"]=out[:100];return state["master_dna_v104"]

def memory_windows(state):
    rows=[x for x in state.get("experience_bank_v104",[]) if x.get("result") in ("WIN","LOSS")]
    def one(n):
        r=rows[-n:] if n else rows; total=len(r);wins=sum(x.get("result")=="WIN" for x in r)
        return {"samples":total,"win_rate":round(wins/total*100,1) if total else 0.0,"avg_return":round(sum(_f(x.get("return_pct")) for x in r)/total,3) if total else 0.0}
    return {"recent_100":one(100),"recent_1000":one(1000),"all":one(0)}

def confidence_forecast(state, signal=None):
    rows=[x for x in state.get("experience_bank_v104",[]) if x.get("result") in ("WIN","LOSS")]
    current=_f((signal or {}).get("confidence"),50.0)
    rates=[]
    for n in (10,20,40):
        r=rows[-n:];rates.append(sum(x.get("result")=="WIN" for x in r)/len(r)*100 if r else 50.0)
    momentum=(rates[0]-rates[-1])*.08; forecast=max(0,min(100,current+momentum))
    direction="RISING" if forecast>current+.5 else "FALLING" if forecast<current-.5 else "STABLE"
    return {"current":round(current,1),"forecast":round(forecast,1),"direction":direction,"basis_samples":min(40,len(rows)),"window_rates":[round(x,1) for x in rates]}

def explain_ai(state,signal):
    f=_features(signal);weights={"volume":.14,"oi":.16,"funding":.10,"compression":.10,"momentum":.14,"pattern":.14,"cycle":.10,"mtf":.12}
    parts=[]
    for k in FEATURES:
        val=f[k];contrib=(val-50)*weights[k]/5
        parts.append({"feature":k,"value":val,"contribution":round(contrib,2),"effect":"POSITIVE" if contrib>.2 else "NEGATIVE" if contrib<-.2 else "NEUTRAL"})
    transfer=cross_coin_learning(state,signal);total=sum(x["contribution"] for x in parts)+transfer["confidence_adjustment"]
    return {"base_confidence":round(_f(signal.get("confidence")),1),"feature_adjustment":round(sum(x["contribution"] for x in parts),2),"cross_coin_adjustment":transfer["confidence_adjustment"],"estimated_confidence":round(max(0,min(100,_f(signal.get("confidence"))+total)),1),"parts":sorted(parts,key=lambda x:abs(x["contribution"]),reverse=True),"transfer":transfer}

def self_optimize(state,min_samples=12,max_step=.02):
    """Bounded advisory optimization. Does not touch execution/order configuration."""
    rows=[x for x in state.get("experience_bank_v104",[]) if x.get("result") in ("WIN","LOSS")][-100:]
    old=dict(state.get("optimization_v104") or {"confidence_bias":0.0,"false_risk_bias":0.0,"tp_multiplier":1.0,"sl_multiplier":1.0,"position_multiplier":1.0})
    if len(rows)<min_samples:return {"changed":False,"reason":"표본 부족","samples":len(rows),"parameters":old,"advisory_only":True}
    wr=sum(x.get("result")=="WIN" for x in rows[-30:])/len(rows[-30:]);avg=sum(_f(x.get("return_pct")) for x in rows[-30:])/len(rows[-30:])
    d=1 if wr>=.58 and avg>0 else -1 if wr<.43 or avg<-.2 else 0;new=dict(old)
    new["confidence_bias"]=round(max(-10,min(10,_f(old.get("confidence_bias"))+d*max_step*100)),2)
    new["false_risk_bias"]=round(max(-10,min(10,_f(old.get("false_risk_bias"))-d*max_step*100)),2)
    new["tp_multiplier"]=round(max(.85,min(1.15,_f(old.get("tp_multiplier"),1)+d*max_step)),4)
    new["sl_multiplier"]=round(max(.85,min(1.15,_f(old.get("sl_multiplier"),1)-d*max_step/2)),4)
    new["position_multiplier"]=round(max(.70,min(1.10,_f(old.get("position_multiplier"),1)+d*max_step/2)),4)
    state["optimization_v104"]=new
    return {"changed":new!=old,"samples":len(rows),"win_rate":round(wr*100,1),"avg_return":round(avg,3),"parameters":new,"advisory_only":True}

def experience_summary(state):
    bank=state.get("experience_bank_v104",[]);dec=[x for x in bank if x.get("result") in ("WIN","LOSS")]
    return {"total":len(bank),"decided":len(dec),"symbols":len({x.get("symbol") for x in bank}),"master_dna":len(state.get("master_dna_v104",[])),"memory":memory_windows(state),"optimization":dict(state.get("optimization_v104") or {})}
