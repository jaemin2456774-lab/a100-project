"""A100 V106.0 Real-Time Intelligence Engine.

Order-free live observation utilities. It records observed snapshots of open
paper/shadow signals, estimates adaptive confidence and signal health, detects
market regimes, aggregates a collective brain, and tracks calibration error.
No live order placement or automatic order-setting mutation exists.
"""
from __future__ import annotations
import hashlib,time,math
from collections import Counter,defaultdict
FEATURES=("volume","oi","funding","compression","momentum","pattern","cycle","mtf")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _s(v):return str(v or "").upper()
def _features(x):
    r=x.get("features") or x.get("signals") or {}
    return {k:round(_f(r.get(k),50),3) for k in FEATURES}
def _open(x):return _s(x.get("status") or x.get("result") or "OPEN") in ("OPEN","ACTIVE","TRACKING","PENDING","LIVE")

def capture_live_memory(state,max_points=24000,min_gap=120):
    bank=list(state.get("live_memory_v106") or []);last={}
    for x in bank:last[str(x.get("source_id"))]=max(last.get(str(x.get("source_id")),0),_f(x.get("captured_at")))
    now=time.time();added=0;active=0
    for key in ("paper_positions","shadow_positions","open_positions","signals","shadow_signals"):
        rows=state.get(key) or []
        if not isinstance(rows,list):continue
        for r in rows:
            if not isinstance(r,dict) or not _open(r):continue
            sid=str(r.get("id") or r.get("signal_id") or r.get("trade_id") or "")
            sym=str(r.get("symbol") or r.get("ticker") or "").upper()
            if not sid or not sym:continue
            active+=1
            if now-last.get(sid,0)<min_gap:continue
            entry=_f(r.get("entry_price") or r.get("entry"));price=_f(r.get("current_price") or r.get("mark_price") or r.get("price"),entry)
            side=_s(r.get("side") or r.get("direction") or "WAIT")
            move=((price-entry)/entry*100 if entry else 0)*( -1 if side=="SHORT" else 1)
            item={"id":"LM-"+hashlib.sha1((sid+str(now)).encode()).hexdigest()[:10].upper(),"source_id":sid,"source":key,"symbol":sym,"side":side,"captured_at":now,"age_min":round(max(0,(now-_f(r.get("opened_at") or r.get("created_at"),now))/60),1),"entry":entry,"price":price,"move_pct":round(move,4),"base_confidence":round(_f(r.get("confidence"),50),2),"features":_features(r)}
            bank.append(item);last[sid]=now;added+=1
    bank.sort(key=lambda x:x.get("captured_at",0));state["live_memory_v106"]=bank[-max_points:]
    return {"added":added,"total":len(state["live_memory_v106"]),"active":active,"signals":len({x.get('source_id') for x in state["live_memory_v106"]})}

def adaptive_confidence(state,symbol=None):
    rows=list(state.get("live_memory_v106") or []);symbol=(symbol or "").upper()
    if symbol: rows=[x for x in rows if x.get("symbol")==symbol]
    if not rows:return {"symbol":symbol or "ALL","current":0.0,"base":0.0,"delta":0.0,"trend":"STABLE","points":0}
    latest={}
    for x in rows:latest[x.get("source_id")]=x
    vals=[]
    for x in latest.values():
        f=x.get("features") or {};strength=sum((_f(f.get(k),50)-50) for k in FEATURES)/len(FEATURES)
        health_move=max(-10,min(10,_f(x.get("move_pct"))*2.5))
        vals.append(max(0,min(100,_f(x.get("base_confidence"),50)+strength*.12+health_move)))
    cur=sum(vals)/len(vals);base=sum(_f(x.get("base_confidence"),50) for x in latest.values())/len(latest);d=cur-base
    return {"symbol":symbol or "ALL","current":round(cur,1),"base":round(base,1),"delta":round(d,1),"trend":"RISING" if d>1 else "FALLING" if d<-1 else "STABLE","points":len(rows)}

def signal_health(state,symbol=None):
    rows=list(state.get("live_memory_v106") or []);symbol=(symbol or "").upper()
    if symbol:rows=[x for x in rows if x.get("symbol")==symbol]
    if not rows:return {"symbol":symbol or "ALL","health":0.0,"grade":"NO DATA","trend":"STABLE","signals":0}
    latest={};first={}
    for x in rows:
        sid=x.get("source_id");first.setdefault(sid,x);latest[sid]=x
    hs=[];deltas=[]
    for sid,x in latest.items():
        f=x.get("features") or {};quality=sum(_f(f.get(k),50) for k in FEATURES)/len(FEATURES)
        move=_f(x.get("move_pct"));age=_f(x.get("age_min"));h=max(0,min(100,50+(quality-50)*.55+max(-20,min(20,move*4))-min(15,age/120)))
        hs.append(h);fx=first[sid];fq=sum(_f((fx.get('features') or {}).get(k),50) for k in FEATURES)/len(FEATURES);fh=max(0,min(100,50+(fq-50)*.55+max(-20,min(20,_f(fx.get('move_pct'))*4)))) ;deltas.append(h-fh)
    v=sum(hs)/len(hs);d=sum(deltas)/len(deltas);grade="A" if v>=85 else "B" if v>=70 else "C" if v>=55 else "D"
    return {"symbol":symbol or "ALL","health":round(v,1),"grade":grade,"trend":"RISING" if d>2 else "FALLING" if d<-2 else "STABLE","signals":len(latest),"delta":round(d,1)}

def detect_regime(state,symbol=None):
    rows=list(state.get("live_memory_v106") or []);symbol=(symbol or "").upper()
    if symbol:rows=[x for x in rows if x.get("symbol")==symbol]
    if not rows:return {"symbol":symbol or "ALL","regime":"UNKNOWN","confidence":0.0,"samples":0,"reasons":[]}
    latest={}
    for x in rows:latest[x.get('source_id')]=x
    rs=list(latest.values());avg=lambda k:sum(_f((x.get('features') or {}).get(k),50) for x in rs)/len(rs)
    mom,vol,comp,oi,fund=avg('momentum'),avg('volume'),avg('compression'),avg('oi'),avg('funding');move=sum(_f(x.get('move_pct')) for x in rs)/len(rs)
    if vol>=75 and move<=-2:reg="PANIC"
    elif oi>=70 and fund<=35 and move>1:reg="SHORT SQUEEZE"
    elif oi>=70 and fund>=65 and move<-1:reg="LONG SQUEEZE"
    elif vol>=70 and abs(move)>=1.5:reg="HIGH VOLATILITY"
    elif comp>=70 and vol<55:reg="LOW VOLATILITY"
    elif abs(mom-50)>=12:reg="TREND"
    else:reg="RANGE"
    conf=min(95,45+abs(mom-50)*.7+abs(vol-50)*.35+len(rs)*1.5)
    return {"symbol":symbol or "ALL","regime":reg,"confidence":round(conf,1),"samples":len(rs),"reasons":[f"momentum {mom:.0f}",f"volume {vol:.0f}",f"OI {oi:.0f}",f"funding {fund:.0f}",f"move {move:+.2f}%"]}

def collective_brain(state):
    rows=list(state.get("live_memory_v106") or []);latest={}
    for x in rows:latest[x.get('source_id')]=x
    syms=defaultdict(list)
    for x in latest.values():syms[x.get('symbol')].append(x)
    regimes=[];confs=[];health=[]
    for sym in syms:
        regimes.append(detect_regime(state,sym)['regime']);confs.append(adaptive_confidence(state,sym)['current']);health.append(signal_health(state,sym)['health'])
    dominant=Counter(regimes).most_common(1)[0][0] if regimes else "UNKNOWN"
    return {"symbols":len(syms),"signals":len(latest),"dominant_regime":dominant,"confidence":round(sum(confs)/len(confs),1) if confs else 0.0,"health":round(sum(health)/len(health),1) if health else 0.0,"regimes":dict(Counter(regimes))}

def accuracy_tracker(state):
    rows=[]
    for k in ('shadow_learning_v105','experience_bank_v104'):
        rows.extend(x for x in (state.get(k) or []) if _s(x.get('result') or x.get('status')) in ('WIN','LOSS'))
    if not rows:return {"samples":0,"predicted":0.0,"actual":0.0,"mae":0.0,"calibration":"NO DATA"}
    pred=sum(_f(x.get('confidence'),50) for x in rows)/len(rows);actual=sum(_s(x.get('result') or x.get('status'))=='WIN' for x in rows)/len(rows)*100;mae=abs(pred-actual)
    return {"samples":len(rows),"predicted":round(pred,1),"actual":round(actual,1),"mae":round(mae,1),"calibration":"GOOD" if mae<=7 else "WATCH" if mae<=15 else "POOR"}

def evolution_dashboard(state):
    return {"memory":capture_live_memory(state),"confidence":adaptive_confidence(state),"health":signal_health(state),"regime":detect_regime(state),"brain":collective_brain(state),"accuracy":accuracy_tracker(state),"experience":len(state.get('experience_bank_v104') or []),"mtf_dna":len(state.get('mtf_dna_v105') or []),"global_dna":len(state.get('global_dna_v105') or []),"weaknesses":len(state.get('weaknesses_v105') or []),"advisory_only":True}
