"""A100 V99.0 Predictive Intelligence analytics.
Read-only deterministic analytics. No network, persistence mutation, or order execution.
"""
from __future__ import annotations


def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d

def clamp(v, lo=0.0, hi=100.0): return max(lo, min(hi, _f(v)))

def grade(s):
    s=_f(s)
    return 'A+' if s>=88 else 'A' if s>=78 else 'B' if s>=66 else 'C' if s>=54 else 'D'

def ai_score(candidate, cycle, health, evolution, calibration, shadow):
    risk=_f((candidate.get('signals') or {}).get('risk'),50)
    cal=clamp(100-abs(_f(calibration.get('error')))*2-_f(calibration.get('mae'))*.25)
    sh=clamp(.72*_f(shadow.get('win_rate'))+.28*min(100,_f(shadow.get('n'))*2))
    score=clamp(.28*_f(candidate.get('probability_v2',candidate.get('probability')))+.20*_f(candidate.get('confidence'))+
                .13*_f(cycle.get('confidence'))+.12*_f(health.get('overall'))+.12*_f(evolution.get('composite'))+
                .08*cal+.07*sh-.10*risk)
    label='STRONG '+str(candidate.get('side','WAIT')) if score>=82 else str(candidate.get('side','WAIT')) if score>=64 else 'WAIT'
    return {'score':round(score,1),'grade':grade(score),'label':label,'calibration_score':round(cal,1),'shadow_score':round(sh,1)}

def multi_timeframe(candidate):
    s=candidate.get('signals') or {}; side=str(candidate.get('side','WAIT')).upper()
    direction=1 if side=='LONG' else -1 if side=='SHORT' else 0
    base=.30*_f(s.get('momentum'))+.25*_f(s.get('volume'))+.20*_f(s.get('oi'))+.15*_f(s.get('compression'))+.10*_f(s.get('similarity'))
    offsets={'15M':3,'1H':1,'4H':-1,'1D':-3}
    frames={}
    for k,o in offsets.items():
        strength=clamp(base+o)
        signed=(strength-50)*direction
        frames[k]={'direction':'▲' if signed>=6 else '▼' if signed<=-6 else '■','strength':round(strength,1)}
    alignment=sum(1 for x in frames.values() if x['direction']==('▲' if direction>=0 else '▼'))
    confidence=clamp(_f(candidate.get('confidence'))*(.75+.0625*alignment))
    return {'frames':frames,'alignment':alignment,'confidence':round(confidence,1),'side':side}

def entry_plan(candidate, ai):
    p=_f(candidate.get('probability_v2',candidate.get('probability'))); risk=_f((candidate.get('signals') or {}).get('risk'),50)
    side=str(candidate.get('side','WAIT')).upper(); quality=_f(ai.get('score'))
    # Relative plan avoids inventing a live price. Values are percentages from a user-confirmed reference price.
    width=round(max(.35,min(2.0,1.35-risk/100)),2)
    stop=round(max(.8,min(4.5,1.2+risk*.025)),2)
    rr1=round(max(1.2,min(2.5,1.25+(quality-50)/45)),2); rr2=round(rr1+max(.6,(p-50)/35),2)
    return {'side':side,'entry_from':-width if side=='LONG' else 0.0,'entry_to':0.0 if side=='LONG' else width,
            'stop_pct':stop,'target1_pct':round(stop*rr1,2),'target2_pct':round(stop*rr2,2),'rr1':rr1,'rr2':rr2,
            'mode':'RELATIVE_TO_REFERENCE_PRICE'}

def explain(candidate, ai, mtf):
    s=candidate.get('signals') or {}
    labels=[('거래량',s.get('volume')),('미결제약정',s.get('oi')),('펀딩 우위',s.get('funding_edge')),
            ('변동성 압축',s.get('compression')),('모멘텀',s.get('momentum')),('유사 패턴',s.get('similarity'))]
    positives=[n for n,v in labels if _f(v)>=60]; cautions=[n for n,v in labels if _f(v)<45]
    return {'positives':positives[:4] or ['뚜렷한 강점 없음'],'cautions':cautions[:3] or ['중대 약점 없음'],
            'summary':f"{ai.get('label','WAIT')} · {mtf.get('alignment',0)}/4 타임프레임 정렬"}

def signal_history(rows, limit=20):
    recent=list(rows or [])[-limit:]
    wins=losses=holds=0
    for r in recent:
        ret=_f(r.get('return_pct',r.get('pnl_pct',r.get('result_pct',0))))
        if ret>.05:wins+=1
        elif ret<-.05:losses+=1
        else:holds+=1
    decided=wins+losses
    return {'n':len(recent),'wins':wins,'losses':losses,'holds':holds,'win_rate':round(wins/decided*100,1) if decided else 0.0}
