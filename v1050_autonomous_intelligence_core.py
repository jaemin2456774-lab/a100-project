"""A100 V105.0 Autonomous Intelligence Core.

Closed-loop, order-free learning utilities. The engine learns only from observed
and resolved paper/shadow outcomes, builds multi-timeframe/global pattern DNA,
tracks confidence growth, discovers weaknesses, compares model snapshots and
runs a bounded closed-loop recommendation cycle. No live order operation exists.
"""
from __future__ import annotations
import hashlib, time
from collections import defaultdict

FEATURES=("volume","oi","funding","compression","momentum","pattern","cycle","mtf")
TIMEFRAMES=("5m","15m","1h","4h","1d")

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _status(x): return str(x or "").upper()

def _features(row):
    raw=row.get("features") or row.get("signals") or {}
    return {k:round(_f(raw.get(k)),4) for k in FEATURES}

def _resolved(row): return _status(row.get("status") or row.get("result")) in ("WIN","LOSS","HOLD")

def capture_shadow_learning(state,max_rows=12000):
    """Capture only observed, resolved shadow/paper records; never invent outcomes."""
    bank=list(state.get("shadow_learning_v105") or []);seen={x.get("source_id") for x in bank};added=0
    sources=[]
    for key in ("shadow_signals","shadow_positions","shadow_history","paper_history","signals"):
        val=state.get(key) or []
        if isinstance(val,list): sources.extend((key,x) for x in val if isinstance(x,dict))
    for source,row in sources:
        sid=str(row.get("id") or row.get("signal_id") or row.get("trade_id") or "")
        if not sid or sid in seen or not _resolved(row): continue
        symbol=str(row.get("symbol") or row.get("ticker") or "").upper()
        if not symbol: continue
        status=_status(row.get("status") or row.get("result"))
        item={"id":"SHL-"+hashlib.sha1((source+sid).encode()).hexdigest()[:10].upper(),"source_id":sid,
              "source":source,"symbol":symbol,"side":_status(row.get("side") or row.get("direction") or "WAIT"),
              "result":status,"return_pct":round(_f(row.get("return_pct") or row.get("pnl_pct")),6),
              "confidence":round(_f(row.get("confidence"),50),3),"features":_features(row),
              "timeframe":str(row.get("timeframe") or row.get("tf") or "unknown"),
              "closed_at":_f(row.get("closed_at") or row.get("updated_at"),time.time())}
        bank.append(item);seen.add(sid);added+=1
    bank.sort(key=lambda x:(x.get("closed_at",0),x.get("id","")))
    state["shadow_learning_v105"]=bank[-max_rows:]
    return {"added":added,"total":len(state["shadow_learning_v105"]),"resolved":sum(x['result'] in ('WIN','LOSS') for x in state["shadow_learning_v105"])}

def build_mtf_dna(state,min_samples=2):
    rows=list(state.get("shadow_learning_v105") or [])+list(state.get("experience_bank_v104") or [])
    groups=defaultdict(list)
    for x in rows:
        tf=str(x.get("timeframe") or "unknown").lower(); tf=tf if tf in TIMEFRAMES else "unknown"
        f=x.get("features") or {}; active=tuple(sorted(k for k,v in f.items() if _f(v)>=60))[:4] or ("neutral",)
        groups[(tf,_status(x.get("side")),active)].append(x)
    out=[]
    for (tf,side,active),rs in groups.items():
        decided=[x for x in rs if _status(x.get("result")) in ("WIN","LOSS")]
        if len(decided)<min_samples: continue
        wins=sum(_status(x.get("result"))=="WIN" for x in decided);wr=wins/len(decided)*100
        sig=f"{tf}|{side}|{'+'.join(active)}"
        out.append({"id":"MTF-"+hashlib.sha1(sig.encode()).hexdigest()[:8].upper(),"timeframe":tf,"side":side,
                    "signature":"+".join(active),"samples":len(decided),"win_rate":round(wr,1),
                    "confidence":round(min(100,len(decided)/15*100),1),"status":"STABLE" if len(decided)>=10 else "FORMING"})
    out.sort(key=lambda x:(TIMEFRAMES.index(x['timeframe']) if x['timeframe'] in TIMEFRAMES else 99,-x['samples'],-x['win_rate']))
    state["mtf_dna_v105"]=out[:300];return state["mtf_dna_v105"]

def build_global_patterns(state,min_symbols=2,min_samples=3):
    rows=list(state.get("shadow_learning_v105") or [])+list(state.get("experience_bank_v104") or [])
    groups=defaultdict(list)
    for x in rows:
        f=x.get("features") or {};active=tuple(sorted(k for k,v in f.items() if _f(v)>=60))[:4] or ("neutral",)
        groups[(_status(x.get("side")),active)].append(x)
    out=[]
    for (side,active),rs in groups.items():
        decided=[x for x in rs if _status(x.get("result")) in ("WIN","LOSS")];symbols={x.get("symbol") for x in decided if x.get("symbol")}
        if len(decided)<min_samples or len(symbols)<min_symbols:continue
        wr=sum(_status(x.get("result"))=="WIN" for x in decided)/len(decided)*100;sig=f"{side}|{'+'.join(active)}"
        out.append({"id":"GDNA-"+hashlib.sha1(sig.encode()).hexdigest()[:8].upper(),"side":side,"signature":"+".join(active),
                    "samples":len(decided),"symbols":len(symbols),"win_rate":round(wr,1),"status":"GLOBAL" if len(symbols)>=4 and len(decided)>=12 else "FORMING"})
    out.sort(key=lambda x:(-x['symbols'],-x['samples'],-x['win_rate']));state["global_dna_v105"]=out[:200];return state["global_dna_v105"]

def record_growth(state):
    rows=[x for x in (list(state.get("shadow_learning_v105") or [])+list(state.get("experience_bank_v104") or [])) if _status(x.get("result")) in ("WIN","LOSS")]
    n=len(rows);wins=sum(_status(x.get("result"))=="WIN" for x in rows);wr=wins/n*100 if n else 0.0
    point={"at":time.time(),"samples":n,"win_rate":round(wr,2),"dna":len(state.get("mtf_dna_v105") or [])+len(state.get("global_dna_v105") or [])}
    hist=list(state.get("growth_history_v105") or [])
    if not hist or (hist[-1].get('samples'),hist[-1].get('win_rate'),hist[-1].get('dna'))!=(point['samples'],point['win_rate'],point['dna']):hist.append(point)
    state["growth_history_v105"]=hist[-120:];return point

def growth_graph(state,width=12):
    hist=list(state.get("growth_history_v105") or [])[-width:]
    if not hist:return {"points":[],"bars":"표본 없음","trend":"STABLE"}
    vals=[_f(x.get("win_rate")) for x in hist];blocks="▁▂▃▄▅▆▇█"
    bars=''.join(blocks[min(7,max(0,int(v/100*8)))] for v in vals)
    trend="RISING" if len(vals)>1 and vals[-1]>vals[0]+1 else "FALLING" if len(vals)>1 and vals[-1]<vals[0]-1 else "STABLE"
    return {"points":hist,"bars":bars,"trend":trend,"latest":vals[-1]}

def discover_weaknesses(state,min_samples=6):
    rows=[x for x in (list(state.get("shadow_learning_v105") or [])+list(state.get("experience_bank_v104") or [])) if _status(x.get("result")) in ("WIN","LOSS")]
    out=[]
    for k in FEATURES:
        rel=[x for x in rows if k in (x.get("features") or {})]
        if len(rel)<min_samples: continue
        bad=[x for x in rel if _status(x.get("result"))=="LOSS"]
        err=len(bad)/len(rel)*100
        avg_loss=sum(_f((x.get("features") or {}).get(k),50) for x in bad)/len(bad) if bad else 0
        severity=err*max(.5,abs(avg_loss-50)/50)
        out.append({"feature":k,"samples":len(rel),"error_rate":round(err,1),"loss_feature_avg":round(avg_loss,1),"severity":round(severity,1)})
    out.sort(key=lambda x:-x['severity']);state["weaknesses_v105"]=out;return out

def snapshot_version(state,version="V105"):
    rows=[x for x in (list(state.get("shadow_learning_v105") or [])+list(state.get("experience_bank_v104") or [])) if _status(x.get("result")) in ("WIN","LOSS")]
    n=len(rows);wr=sum(_status(x.get("result"))=="WIN" for x in rows)/n*100 if n else 0
    avg=sum(_f(x.get("return_pct")) for x in rows)/n if n else 0
    snaps=dict(state.get("model_snapshots_v105") or {});snaps[version]={"samples":n,"win_rate":round(wr,1),"avg_return":round(avg,3),"captured_at":time.time()};state["model_snapshots_v105"]=snaps
    return snaps

def compare_versions(state):
    snaps=snapshot_version(state,"V105");order=sorted(snaps)
    rows=[dict(version=k,**snaps[k]) for k in order]
    regression=False
    if len(rows)>=2 and rows[-1]['samples']>=rows[-2]['samples'] and rows[-1]['win_rate']<rows[-2]['win_rate']-3:regression=True
    return {"rows":rows,"regression":regression}

def closed_loop_cycle(state):
    shadow=capture_shadow_learning(state);mtf=build_mtf_dna(state);glob=build_global_patterns(state);weak=discover_weaknesses(state);growth=record_growth(state);comp=compare_versions(state)
    decided=shadow['resolved'];ready=decided>=12
    recommendation={"confidence_bias":0.0,"false_risk_bias":0.0,"tp_multiplier":1.0,"sl_multiplier":1.0,"position_multiplier":1.0}
    if ready:
        top=weak[0] if weak else None
        recommendation["confidence_bias"]=-1.0 if top and top['error_rate']>55 else 0.5
        recommendation["false_risk_bias"]=1.0 if top and top['error_rate']>55 else -0.5
        recommendation["position_multiplier"]=.95 if comp['regression'] else 1.0
    state["closed_loop_recommendation_v105"]={"ready":ready,"samples":decided,"parameters":recommendation,"advisory_only":True,"updated_at":time.time()}
    return {"shadow":shadow,"mtf":len(mtf),"global":len(glob),"weaknesses":len(weak),"growth":growth,"comparison":comp,"recommendation":state["closed_loop_recommendation_v105"]}

def summary(state):
    return {"shadow":len(state.get("shadow_learning_v105") or []),"mtf_dna":len(state.get("mtf_dna_v105") or []),"global_dna":len(state.get("global_dna_v105") or []),"growth":growth_graph(state),"weaknesses":list(state.get("weaknesses_v105") or []),"versions":compare_versions(state),"closed_loop":dict(state.get("closed_loop_recommendation_v105") or {})}
