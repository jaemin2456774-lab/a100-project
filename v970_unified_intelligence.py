"""A100 V97.0 Unified Intelligence and Early Pump analytics.
Read-only, deterministic analytics. No network calls, order execution, or state mutation.
"""
from __future__ import annotations
from datetime import datetime, timezone


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d

def clamp(v, lo=0.0, hi=100.0): return max(lo, min(hi, _f(v)))

def _component(item, *names, default=50.0):
    c=item.get("components") or {}
    lower={str(k).lower():v for k,v in c.items()}
    for n in names:
        if n in c: return _f(c[n], default)
        if str(n).lower() in lower: return _f(lower[str(n).lower()], default)
    return default

def classify_regime(rows, memory):
    one=memory.get("1D",{}); seven=memory.get("7D",{}); thirty=memory.get("30D",{})
    avg=_f(one.get("avg")); wr=_f(one.get("win_rate")); n=int(one.get("n",0))
    drift=wr-_f(thirty.get("win_rate")); long_avg=_f(seven.get("avg"))
    if n < 5: regime="DATA_THIN"
    elif avg >= .45 and wr >= 58: regime="BULL_EXPANSION"
    elif avg <= -.45 and wr <= 42: regime="BEAR_STRESS"
    elif abs(avg) <= .15 and abs(long_avg) <= .20: regime="RANGE_COMPRESSION"
    elif abs(avg) >= .80: regime="VOLATILITY_EXPANSION"
    else: regime="TRANSITION"
    risk="HIGH" if regime in {"BEAR_STRESS","VOLATILITY_EXPANSION","DATA_THIN"} else "LOW" if regime=="BULL_EXPANSION" else "MEDIUM"
    score=clamp(50 + avg*18 + (wr-50)*.7 + drift*.25)
    return {"regime":regime,"risk":risk,"score":round(score,1),"sample":n,"drift":round(drift,1)}

def early_pump_score(item, similarity, quality=0.0, calibration=None, regime=None):
    calibration=calibration or {}; regime=regime or {}
    vol=_component(item,"Volume","volume","Volume Expansion",default=50)
    oi=_component(item,"OI","Open Interest","open_interest",default=50)
    funding=_component(item,"Funding","funding",default=50)
    compression=_component(item,"Volatility","Compression","volatility",default=50)
    momentum=_component(item,"Momentum","Trend","momentum",default=50)
    liquidity=_component(item,"Liquidity","liquidity",default=50)
    risk=_component(item,"Risk","risk",default=50)
    sim=_f(similarity.get("avg_similarity")); hist_wr=_f(similarity.get("win_rate")); n=int(similarity.get("n",0))
    conf=clamp(item.get("confidence",item.get("score",50)) + _f(calibration.get("adjustment")))
    # Negative/neutral funding is favorable. Components are normalized quality scores where available.
    funding_edge=clamp(100-abs(funding-45)*1.1)
    evidence=clamp(n/20*100)
    raw=(.16*vol+.14*oi+.11*funding_edge+.12*compression+.13*momentum+.08*liquidity+
         .11*sim+.07*hist_wr+.05*_f(quality)+.06*conf+.05*evidence-.08*risk)
    regime_name=str(regime.get("regime",""))
    modifier=4 if regime_name=="BULL_EXPANSION" else -7 if regime_name in {"BEAR_STRESS","DATA_THIN"} else 0
    score=clamp(raw+modifier)
    grade="A+" if score>=82 else "A" if score>=74 else "B" if score>=64 else "C" if score>=54 else "D"
    action="PAPER" if score>=76 and n>=5 else "WATCH" if score>=62 else "AVOID"
    return {"symbol":str(item.get("symbol","?")),"side":str(item.get("side","WAIT")),"probability":round(score,1),
            "grade":grade,"action":action,"confidence":round(conf,1),"sample":n,
            "signals":{"volume":round(vol,1),"oi":round(oi,1),"funding_edge":round(funding_edge,1),
                       "compression":round(compression,1),"momentum":round(momentum,1),"similarity":round(sim,1),"risk":round(risk,1)}}

def growth_report(memory, calibration, shadow, health):
    def window_score(x):
        n=int(x.get("n",0)); wr=_f(x.get("win_rate")); avg=_f(x.get("avg"))
        return clamp(.55*wr + .25*clamp(50+avg*12) + .20*clamp(n/100*100))
    scores={k:round(window_score(memory.get(k,{})),1) for k in ("1D","7D","30D","ALL")}
    cal_score=clamp(100-abs(_f(calibration.get("error")))*2-_f(calibration.get("mae"))*.35)
    shadow_score=clamp(.65*_f(shadow.get("win_rate"))+.35*clamp(int(shadow.get("n",0))/100*100))
    overall=clamp(.35*scores["7D"]+.25*scores["30D"]+.20*cal_score+.20*shadow_score)
    trend=scores["1D"]-scores["7D"]
    direction="IMPROVING" if trend>=3 else "WEAKENING" if trend<=-3 else "STABLE"
    return {"overall":round(overall,1),"direction":direction,"trend":round(trend,1),"windows":scores,
            "calibration":round(cal_score,1),"shadow":round(shadow_score,1),"health":round(_f(health.get("overall")),1)}

def self_heal_advice(memory, calibration, shadow, health):
    actions=[]
    if abs(_f(calibration.get("error")))>8: actions.append("CONFIDENCE_RECALIBRATE")
    if _f(memory.get("1D",{}).get("win_rate")) + 8 < _f(memory.get("30D",{}).get("win_rate")): actions.append("RECENT_PATTERN_DECAY")
    if int(shadow.get("n",0))<30: actions.append("SHADOW_SAMPLE_BUILD")
    if _f(health.get("consistency"))<65: actions.append("WEIGHT_STABILIZE")
    if not actions: actions.append("NO_CHANGE")
    return {"mode":"ADVISORY_ONLY","actions":actions,"safe":True,"generated_at":datetime.now(timezone.utc).isoformat()}
