"""A100 V108.0 Pattern Recognition Intelligence.
Pattern abstraction, naming, quality tracking, shadow history, and market memory.
Observation/learning only. No live order execution.
"""
from __future__ import annotations
import hashlib, math, time
from collections import Counter, defaultdict

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _s(v):return str(v or '').upper()

def _features(row):
    x=row.get('features') or row.get('signals') or {}
    out={k:_f(x.get(k),50.0) for k in ('volume','oi','funding','compression','momentum','pattern','cycle','mtf')}
    # allow flattened historical records
    for k in tuple(out):
        if k in row: out[k]=_f(row.get(k),out[k])
    return out

def classify_pattern(row):
    f=_features(row); side=_s(row.get('side') or row.get('direction'))
    vol,oi,fun,comp,mom,pat,cyc,mtf=(f[k] for k in ('volume','oi','funding','compression','momentum','pattern','cycle','mtf'))
    # deterministic, explainable precedence
    if comp>=70 and vol>=65 and mom>=60: name='COMPRESSION BREAKOUT'
    elif oi>=68 and vol>=62 and mom>=58: name='LIQUIDITY BREAKOUT'
    elif fun>=70 and side=='SHORT': name='FUNDING TRAP'
    elif fun<=30 and side=='LONG': name='NEGATIVE FUNDING REVERSAL'
    elif oi>=70 and fun>=65 and side=='SHORT': name='LONG SQUEEZE SETUP'
    elif oi>=70 and fun<=35 and side=='LONG': name='SHORT SQUEEZE SETUP'
    elif vol>=70 and mom<=38: name='VOLUME FAKEOUT'
    elif pat>=70 and mtf>=62 and mom>=55: name='TREND CONTINUATION'
    elif cyc<=35 and mom>=65: name='CYCLE REVERSAL'
    elif abs(mom-50)<=8 and vol<=45: name='RANGE MEAN REVERSION'
    elif mom>=62: name='HIGH MOMENTUM'
    elif mom<=38: name='BEAR MOMENTUM'
    else: name='UNCLASSIFIED'
    scores=sorted(((k,abs(v-50)) for k,v in f.items()),key=lambda x:x[1],reverse=True)
    strength=min(100.0, max(0.0, 40.0+sum(x[1] for x in scores[:3])*.8))
    signature='|'.join([name,side]+[f'{k}:{int(round(f[k]/10)*10)}' for k in sorted(f)])
    pid='PAT-'+hashlib.sha1(signature.encode()).hexdigest()[:10].upper()
    return {'pattern_id':pid,'name':name,'side':side or 'UNKNOWN','confidence':round(strength,1),'features':f,'evidence':[k for k,_ in scores[:3]]}

def build_pattern_library(state,max_patterns=1000):
    rows=[]
    for key in ('shadow_learning_v105','experience_bank_v104','autonomous_market_scans_v107'):
        rows += [x for x in (state.get(key) or []) if isinstance(x,dict)]
    groups=defaultdict(list)
    for r in rows:
        p=classify_pattern(r); groups[p['pattern_id']].append((r,p))
    old={x.get('pattern_id'):x for x in (state.get('pattern_library_v108') or [])}
    out=[]
    for pid,items in groups.items():
        base=items[0][1]; resolved=[]; symbols=set()
        for r,_ in items:
            res=_s(r.get('result') or r.get('status'))
            if res in ('WIN','LOSS'): resolved.append(1 if res=='WIN' else 0)
            sym=_s(r.get('symbol') or r.get('ticker'))
            if sym:symbols.add(sym)
        samples=len(items); wins=sum(resolved); wr=(wins/len(resolved)*100) if resolved else 0.0
        prior=old.get(pid) or {}; first=prior.get('first_seen') or time.time()
        quality=min(100, samples*5 + len(symbols)*8 + (20 if len(resolved)>=3 else 0) + (wr*.25 if resolved else 0))
        out.append({'pattern_id':pid,'name':base['name'],'side':base['side'],'samples':samples,'resolved':len(resolved),'wins':wins,'win_rate':round(wr,1),'confidence':round(sum(p['confidence'] for _,p in items)/samples,1),'quality':round(quality,1),'symbols':sorted(symbols),'first_seen':first,'last_seen':time.time(),'evidence':base['evidence']})
    out.sort(key=lambda x:(x['quality'],x['samples']),reverse=True)
    state['pattern_library_v108']=out[:max_patterns]
    return {'patterns':len(out),'classified':sum(x['name']!='UNCLASSIFIED' for x in out),'rows':out[:10]}

def detect_pattern(state,symbol):
    sym=_s(symbol); candidates=[]
    for key in ('signals','shadow_signals','paper_positions','shadow_positions','autonomous_market_scans_v107'):
        candidates += [x for x in (state.get(key) or []) if isinstance(x,dict) and _s(x.get('symbol') or x.get('ticker'))==sym]
    if not candidates:return {'symbol':sym,'found':False,'pattern_id':'-','name':'NO DATA','confidence':0.0,'evidence':[]}
    p=classify_pattern(candidates[-1]);p.update({'symbol':sym,'found':True});return p

def pattern_stats(state):
    lib=state.get('pattern_library_v108') or []
    resolved=sum(_f(x.get('resolved')) for x in lib);wins=sum(_f(x.get('wins')) for x in lib)
    named=sum(x.get('name')!='UNCLASSIFIED' for x in lib)
    return {'patterns':len(lib),'named':named,'resolved':int(resolved),'win_rate':round(wins/resolved*100,1) if resolved else 0.0,'top':lib[:8]}

def shadow_history(state,limit=10):
    rows=[]
    for i,r in enumerate(state.get('shadow_learning_v105') or [],1):
        if not isinstance(r,dict):continue
        p=classify_pattern(r)
        rows.append({'no':i,'source_id':r.get('source_id') or r.get('id') or '-', 'symbol':_s(r.get('symbol')),'side':_s(r.get('side') or r.get('direction')),'result':_s(r.get('result') or r.get('status')),'confidence':_f(r.get('confidence')),'pattern_id':p['pattern_id'],'pattern':p['name'],'captured_at':r.get('captured_at') or r.get('closed_at') or 0})
    return {'total':len(rows),'rows':rows[-limit:][::-1]}

def dna_quality(state):
    rows=[]
    for kind,key in (('MTF','mtf_dna_v105'),('GLOBAL','global_dna_v105'),('MASTER','master_dna_v104')):
        for i,x in enumerate(state.get(key) or []):
            if not isinstance(x,dict):continue
            n=int(_f(x.get('samples') or x.get('sample_count') or x.get('count')))
            wr=_f(x.get('win_rate')); symbols=x.get('symbols') or []
            q=min(100,n*8+(15 if n>=3 else 0)+(15 if isinstance(symbols,list) and len(symbols)>=2 else 0)+wr*.25)
            rows.append({'dna_id':x.get('id') or x.get('dna_id') or f'{kind}-{i+1}','kind':kind,'samples':n,'win_rate':wr,'quality':round(q,1),'grade':'A' if q>=80 else 'B' if q>=60 else 'C' if q>=40 else 'FORMING'})
    rows.sort(key=lambda x:x['quality'],reverse=True)
    state['dna_quality_v108']=rows
    return {'total':len(rows),'a_grade':sum(x['grade']=='A' for x in rows),'rows':rows[:10]}

def market_memory(state,max_rows=50000):
    bank=list(state.get('market_memory_v108') or []); seen={x.get('memory_id') for x in bank};added=0
    for r in state.get('autonomous_market_scans_v107') or []:
        if not isinstance(r,dict):continue
        p=classify_pattern(r); bucket=int(_f(r.get('captured_at'),time.time())//900)
        mid='MEM-'+hashlib.sha1(f"{_s(r.get('symbol'))}|{p['pattern_id']}|{bucket}".encode()).hexdigest()[:12].upper()
        if mid in seen:continue
        bank.append({'memory_id':mid,'symbol':_s(r.get('symbol')),'pattern_id':p['pattern_id'],'pattern':p['name'],'confidence':p['confidence'],'captured_at':r.get('captured_at') or time.time(),'price':_f(r.get('price'))});seen.add(mid);added+=1
    state['market_memory_v108']=bank[-max_rows:]
    return {'added':added,'total':len(state['market_memory_v108']),'symbols':len({x.get('symbol') for x in bank if x.get('symbol')}),'patterns':len({x.get('pattern_id') for x in bank if x.get('pattern_id')})}

def intelligence_cycle(state):
    lib=build_pattern_library(state); stats=pattern_stats(state); shadow=shadow_history(state); dq=dna_quality(state); mem=market_memory(state)
    named_ratio=(stats['named']/stats['patterns']*100) if stats['patterns'] else 0
    score=min(100, named_ratio*.25 + min(100,shadow['total']*2)*.2 + min(100,dq['total']*5)*.2 + min(100,mem['total']*.5)*.2 + stats['win_rate']*.15)
    state['pattern_intelligence_v108']={'updated_at':time.time(),'score':round(score,1),'level':1+int(score//20),'patterns':stats['patterns'],'named_ratio':round(named_ratio,1),'shadow':shadow['total'],'dna':dq['total'],'memory':mem['total']}
    return {'library':lib,'stats':stats,'shadow':shadow,'dna_quality':dq,'memory':mem,'intelligence':state['pattern_intelligence_v108'],'advisory_only':True}
