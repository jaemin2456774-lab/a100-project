"""A100 V101.0 Closed Loop Learning Core.

Persistent recommendation capture -> result reconciliation -> bounded feature-weight
learning. The module is network-free and never places or modifies orders.
"""
from __future__ import annotations
import json, os, time, hashlib
from collections import defaultdict

SCHEMA = 1
FEATURES = ("volume", "oi", "funding", "compression", "momentum", "pattern", "cycle", "mtf")


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d


def _ts(row):
    for key in ("closed_at", "exit_time", "timestamp", "time", "created_at", "opened_at"):
        v=row.get(key)
        if v is None: continue
        try:
            x=float(v)
            return x/1000 if x > 10_000_000_000 else x
        except Exception: pass
    return 0.0


def _ret(row):
    for key in ("realized_pct", "return_pct", "pnl_pct", "result_pct"):
        if row.get(key) is not None: return _f(row.get(key))
    n=abs(_f(row.get("notional"))); p=_f(row.get("realized_pnl"))
    return p/n*100 if n else p


def default_state():
    return {"schema":SCHEMA,"signals":[],"weights":{k:1.0 for k in FEATURES},
            "strategies":{},"blacklist":[],"events":[],"updated_at":time.time()}


def load_state(path):
    if not os.path.exists(path): return default_state()
    try:
        with open(path,"r",encoding="utf-8") as f: obj=json.load(f)
        if not isinstance(obj,dict) or obj.get("schema") != SCHEMA: return default_state()
        base=default_state(); base.update(obj)
        if not isinstance(base.get("signals"),list): base["signals"]=[]
        if not isinstance(base.get("weights"),dict): base["weights"]={k:1.0 for k in FEATURES}
        for k in FEATURES: base["weights"].setdefault(k,1.0)
        return base
    except Exception:
        return default_state()


def save_state(path, state):
    os.makedirs(os.path.dirname(os.path.abspath(path)),exist_ok=True)
    state["updated_at"]=time.time(); tmp=path+".tmp"
    with open(tmp,"w",encoding="utf-8") as f:
        json.dump(state,f,ensure_ascii=False,indent=2,sort_keys=True); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)


def _feature_snapshot(candidate, mtf=None, reasons=None):
    sig=candidate.get("signals") or {}; text=" ".join(reasons or []).lower()
    aliases={
      "volume":("volume","거래량"), "oi":("oi","미결제"), "funding":("funding","펀딩"),
      "compression":("compression","압축","변동성"), "momentum":("momentum","모멘텀"),
      "pattern":("pattern","패턴","similar"), "cycle":("cycle","국면"), "mtf":("mtf","타임프레임")}
    out={}
    for key in FEATURES:
        raw=sig.get(key)
        if raw is None:
            raw=1.0 if any(a in text for a in aliases[key]) else 0.0
        raw=_f(raw)
        out[key]=max(0.0,min(100.0, raw if abs(raw)>1 else raw*100))
    if mtf: out["mtf"]=max(out["mtf"],_f(mtf.get("alignment"))*25)
    return out


def capture_signal(state, candidate, score=None, mtf=None, entry=None, reasons=None, now=None, dedupe_seconds=1800):
    now=_f(now,time.time()); symbol=str(candidate.get("symbol") or "").upper(); side=str(candidate.get("side") or "WAIT").upper()
    if not symbol: raise ValueError("symbol required")
    for s in reversed(state["signals"][-100:]):
        if s.get("symbol")==symbol and s.get("side")==side and s.get("status")=="OPEN" and now-_f(s.get("created_at"))<dedupe_seconds:
            return s, False
    base=f"{symbol}|{side}|{now:.6f}|{len(state['signals'])}".encode()
    row={"id":hashlib.sha1(base).hexdigest()[:16],"created_at":now,"symbol":symbol,"side":side,"status":"OPEN",
         "confidence":_f(candidate.get("confidence")),"pump":_f(candidate.get("probability_v2",candidate.get("probability"))),
         "ai_score":_f((score or {}).get("score")),"label":str((score or {}).get("label") or candidate.get("decision") or "WATCH"),
         "features":_feature_snapshot(candidate,mtf,reasons),"entry_plan":dict(entry or {}),"reasons":list(reasons or [])[:8]}
    state["signals"].append(row); state["signals"]=state["signals"][-5000:]
    state["events"].append({"at":now,"kind":"CAPTURE","signal_id":row["id"],"symbol":symbol,"side":side})
    state["events"]=state["events"][-1000:]
    return row, True


def reconcile_outcomes(state, outcome_rows, now=None):
    now=_f(now,time.time()); matched=0
    rows=sorted([r for r in outcome_rows if isinstance(r,dict)],key=_ts)
    used={s.get("outcome_key") for s in state["signals"] if s.get("outcome_key")}
    for r in rows:
        symbol=str(r.get("symbol") or "").upper(); side=str(r.get("side") or "").upper(); closed=_ts(r) or now
        key=f"{symbol}|{side}|{closed:.3f}|{_ret(r):.6f}"
        if not symbol or key in used: continue
        candidates=[s for s in state["signals"] if s.get("status")=="OPEN" and s.get("symbol")==symbol and
                    (not side or s.get("side")==side) and _f(s.get("created_at"))<=closed]
        if not candidates: continue
        s=max(candidates,key=lambda x:_f(x.get("created_at")))
        ret=_ret(r); s.update({"status":"WIN" if ret>.05 else "LOSS" if ret<-.05 else "HOLD",
            "closed_at":closed,"return_pct":round(ret,6),"outcome_key":key,"source":r.get("sample_type","PAPER")})
        used.add(key); matched+=1
        state["events"].append({"at":now,"kind":"OUTCOME","signal_id":s["id"],"result":s["status"],"return_pct":ret})
    return matched


def learn(state, min_samples=5, step=0.03):
    decided=[s for s in state["signals"] if s.get("status") in ("WIN","LOSS")]
    old=dict(state.get("weights") or {}); weights={k:_f(old.get(k),1.0) for k in FEATURES}
    for feature in FEATURES:
        active=[s for s in decided if _f((s.get("features") or {}).get(feature))>=50]
        if len(active)<min_samples: continue
        wr=sum(s["status"]=="WIN" for s in active)/len(active)
        delta=max(-step,min(step,(wr-.5)*step*2))
        weights[feature]=round(max(.50,min(1.50,weights[feature]+delta)),4)
    groups=defaultdict(list)
    for s in decided: groups[f"{s.get('side','?')}|{s.get('label','?')}"] .append(s)
    strategies={}; blacklist=[]
    for name,items in groups.items():
        wins=sum(x["status"]=="WIN" for x in items); n=len(items); wr=wins/n*100 if n else 0
        avg=sum(_f(x.get("return_pct")) for x in items)/n if n else 0
        status="DISABLED" if n>=8 and wr<30 else "WATCH" if n>=5 and wr<45 else "ACTIVE"
        strategies[name]={"n":n,"wins":wins,"losses":n-wins,"win_rate":round(wr,1),"avg_return":round(avg,3),"status":status}
        if status=="DISABLED": blacklist.append(name)
    state["weights"]=weights; state["strategies"]=strategies; state["blacklist"]=sorted(blacklist)
    state["events"].append({"at":time.time(),"kind":"LEARN","decided":len(decided),"changed":sum(abs(weights[k]-_f(old.get(k),1))>.0001 for k in FEATURES)})
    return summary(state)


def summary(state):
    signals=state.get("signals",[]); wins=sum(s.get("status")=="WIN" for s in signals); losses=sum(s.get("status")=="LOSS" for s in signals)
    holds=sum(s.get("status")=="HOLD" for s in signals); opened=sum(s.get("status")=="OPEN" for s in signals); decided=wins+losses
    return {"total":len(signals),"open":opened,"wins":wins,"losses":losses,"holds":holds,
            "win_rate":round(wins/decided*100,1) if decided else 0.0,"weights":dict(state.get("weights") or {}),
            "strategies":dict(state.get("strategies") or {}),"blacklist":list(state.get("blacklist") or [])}
