"""A100 V95.0 AI Unified Dashboard helpers.
Pure formatting and analytics. No network, state mutation, scheduler, or trading path.
"""
from __future__ import annotations

FULL='█'; EMPTY='░'

def clamp(v, lo=0.0, hi=100.0):
    try: v=float(v)
    except Exception: v=0.0
    return max(lo,min(hi,v))

def bar(v,width=10,maximum=100.0):
    width=max(6,min(16,int(width)))
    maximum=float(maximum) if maximum else 100.0
    ratio=clamp(float(v)/maximum*100.0)/100.0
    n=int(round(ratio*width))
    return FULL*n+EMPTY*(width-n)

def aligned_line(label,value,*,width=10,maximum=100.0,count=None,extra=''):
    label=str(label)[:12]
    tail=f'{float(value):5.1f}%'
    if count is not None: tail+=f' · {int(count)}건'
    if extra: tail+=f' · {extra}'
    return f'<code>{label:<12} {bar(value,width,maximum)} {tail}</code>'

def signed_line(label,value,*,width=10,limit=10.0,extra=''):
    try:value=float(value)
    except Exception:value=0.0
    mag=min(abs(value),limit)/limit*100.0
    sign='+' if value>0 else ('-' if value<0 else '±')
    tail=f'{sign}{abs(value):.1f}'
    if extra: tail+=f' · {extra}'
    return f'<code>{str(label)[:12]:<12} {bar(mag,width)} {tail}</code>'

def health_breakdown(sample_count,win_rate,avg_return,completion,engine_samples):
    sample=clamp(sample_count/150*100)
    performance=clamp(.7*win_rate+.3*clamp(50+avg_return*10))
    learning=clamp(engine_samples/100*100)
    integrity=clamp(completion)
    total=clamp(.30*sample+.30*performance+.20*learning+.20*integrity)
    return {'health':round(total,1),'sample':round(sample,1),'performance':round(performance,1),
            'learning':round(learning,1),'integrity':round(integrity,1)}
