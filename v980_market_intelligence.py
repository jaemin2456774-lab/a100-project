"""A100 V98.0 Market Intelligence analytics.
Pure read-only calculations: no network, order execution, or persistent state mutation.
"""
from __future__ import annotations
from math import exp


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d

def clamp(v, lo=0.0, hi=100.0): return max(lo, min(hi, _f(v)))

def grade(score):
    s=_f(score)
    return "A+" if s>=88 else "A" if s>=78 else "B" if s>=66 else "C" if s>=54 else "D"

def level(score):
    s=_f(score)
    return "VERY HIGH" if s>=85 else "HIGH" if s>=72 else "MEDIUM" if s>=55 else "LOW"

def health_grade(score): return grade(score)

def market_cycle(regime, memory, growth):
    name=str(regime.get('regime','TRANSITION'))
    mapping={
        'BULL_EXPANSION':('MARKUP','공격적 후보 선별',1.08),
        'BEAR_STRESS':('MARKDOWN','방어·숏 우선',0.78),
        'RANGE_COMPRESSION':('ACCUMULATION','압축 돌파 감시',1.03),
        'VOLATILITY_EXPANSION':('DISTRIBUTION','추격 금지·변동성 관리',0.86),
        'DATA_THIN':('UNKNOWN','표본 축적 우선',0.72),
        'TRANSITION':('TRANSITION','확인 신호 대기',0.94),
    }
    cycle,policy,mult=mapping.get(name,mapping['TRANSITION'])
    one=memory.get('1D',{}); seven=memory.get('7D',{})
    momentum=clamp(50+(_f(one.get('avg'))*18)+(_f(one.get('win_rate'))-_f(seven.get('win_rate')))*1.2)
    confidence=clamp(.55*_f(regime.get('score'))+.25*_f(growth.get('overall'))+.20*momentum)
    return {'cycle':cycle,'policy':policy,'multiplier':mult,'confidence':round(confidence,1),
            'grade':grade(confidence),'momentum':round(momentum,1),'risk':regime.get('risk','MEDIUM')}

def pump_probability_v2(base, cycle, similarity=None):
    similarity=similarity or {}
    signals=base.get('signals') or {}
    evidence=clamp(_f(base.get('sample'))/40*100)
    signal_strength=(.20*_f(signals.get('volume'))+.18*_f(signals.get('oi'))+.14*_f(signals.get('funding_edge'))+
                     .16*_f(signals.get('compression'))+.16*_f(signals.get('momentum'))+.10*_f(signals.get('similarity'))+
                     .06*evidence)
    calibrated=clamp(.58*_f(base.get('probability'))+.32*signal_strength+.10*_f(base.get('confidence')))
    calibrated=clamp(50+(calibrated-50)*_f(cycle.get('multiplier'),1.0))
    # Conservative ranges, analytics only—not price promises.
    eta='6~18시간' if calibrated>=82 else '12~36시간' if calibrated>=70 else '24~72시간' if calibrated>=58 else '미정'
    low=max(0,round((calibrated-48)*.35,1)); high=max(low,round((calibrated-42)*.75,1))
    if calibrated<58: low=high=0.0
    action='PAPER' if calibrated>=78 and int(base.get('sample',0))>=5 else 'WATCH' if calibrated>=60 else 'AVOID'
    return dict(base, probability_v2=round(calibrated,1), pump_level=level(calibrated), eta=eta,
                expected_move=(low,high), action_v2=action, grade_v2=grade(calibrated), evidence=round(evidence,1))

def evolution_weights(memory):
    # Recency-aware blend. Weights change with sample sufficiency but never mutate stored data.
    ns={k:max(0,int(memory.get(k,{}).get('n',0))) for k in ('1D','7D','30D','ALL')}
    raw={'1D':1.45*(1-exp(-ns['1D']/15)), '7D':1.15*(1-exp(-ns['7D']/40)),
         '30D':.85*(1-exp(-ns['30D']/100)), 'ALL':.45*(1-exp(-ns['ALL']/200))}
    total=sum(raw.values()) or 1
    weights={k:round(v/total*100,1) for k,v in raw.items()}
    scores={k:round(.65*_f(memory.get(k,{}).get('win_rate'))+.35*clamp(50+_f(memory.get(k,{}).get('avg'))*15),1) for k in raw}
    composite=round(sum(scores[k]*weights[k]/100 for k in raw),1)
    return {'weights':weights,'scores':scores,'composite':composite,'grade':grade(composite)}

def portfolio_rank(candidates, cycle, max_slots=5):
    ranked=[]
    for x in candidates:
        p=_f(x.get('probability_v2',x.get('probability'))); conf=_f(x.get('confidence'))
        risk=_f((x.get('signals') or {}).get('risk'),50); evidence=_f(x.get('evidence'))
        utility=clamp(.52*p+.23*conf+.15*evidence+.10*(100-risk))
        allocation=max(0.0,(utility-50))*_f(cycle.get('multiplier'),1.0)
        ranked.append(dict(x,utility=round(utility,1),allocation_raw=allocation,portfolio_grade=grade(utility)))
    ranked.sort(key=lambda z:z['utility'],reverse=True); ranked=ranked[:max_slots]
    denom=sum(z['allocation_raw'] for z in ranked) or 1
    for z in ranked: z['allocation_pct']=round(z['allocation_raw']/denom*100,1) if z['utility']>=58 else 0.0
    return ranked
