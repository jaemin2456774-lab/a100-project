"""A100 V107.0 Autonomous Market Intelligence.
Observation-only autonomous market learning helpers. No live order execution.
"""
from __future__ import annotations
import time, hashlib
from collections import Counter, defaultdict

def _f(v,d=0.0):
    try:return float(v)
    except Exception:return d

def _s(v):return str(v or '').upper()

def auto_market_scan(state, symbols=None, max_rows=50000):
    symbols=[_s(x) for x in (symbols or state.get('watch_symbols') or ['BTCUSDT','ETHUSDT','SOLUSDT','XRPUSDT','BNBUSDT'])]
    sources=[]
    for key in ('market_snapshots','scanner_results','candidates','signals','shadow_signals'):
        rows=state.get(key) or []
        if isinstance(rows,list): sources += [x for x in rows if isinstance(x,dict)]
    now=time.time(); bank=list(state.get('autonomous_market_scans_v107') or []); added=0
    existing={(x.get('symbol'),int(_f(x.get('captured_at'))//300)) for x in bank}
    for sym in symbols:
        candidates=[x for x in sources if _s(x.get('symbol') or x.get('ticker'))==sym]
        r=candidates[-1] if candidates else {}
        bucket=int(now//300)
        if (sym,bucket) in existing: continue
        feat=r.get('features') or r.get('signals') or {}
        item={'id':'AMS-'+hashlib.sha1((sym+str(bucket)).encode()).hexdigest()[:10].upper(),'symbol':sym,'captured_at':now,
              'price':_f(r.get('price') or r.get('mark_price') or r.get('current_price')),
              'confidence':_f(r.get('confidence'),0),'features':{k:_f(feat.get(k),50) for k in ('volume','oi','funding','compression','momentum','pattern','cycle','mtf')}}
        bank.append(item);added+=1
    state['autonomous_market_scans_v107']=bank[-max_rows:]
    return {'added':added,'total':len(state['autonomous_market_scans_v107']),'symbols':len({x.get('symbol') for x in state['autonomous_market_scans_v107']})}

def regime_history(state, detector):
    rows=list(state.get('regime_history_v107') or []);now=time.time();added=0
    symbols=sorted({x.get('symbol') for x in state.get('autonomous_market_scans_v107',[]) if x.get('symbol')})
    for sym in symbols:
        x=detector(state,sym);last=next((r for r in reversed(rows) if r.get('symbol')==sym),None)
        if not last or last.get('regime')!=x.get('regime') or now-_f(last.get('captured_at'))>=1800:
            rows.append({'symbol':sym,'regime':x.get('regime','UNKNOWN'),'confidence':_f(x.get('confidence')),'captured_at':now});added+=1
    state['regime_history_v107']=rows[-20000:]
    return {'added':added,'total':len(state['regime_history_v107']),'changes':sum(1 for a,b in zip(rows,rows[1:]) if a.get('symbol')==b.get('symbol') and a.get('regime')!=b.get('regime'))}

def confidence_calibration(state):
    rows=[]
    for k in ('shadow_learning_v105','experience_bank_v104'):
        rows += [x for x in (state.get(k) or []) if _s(x.get('result') or x.get('status')) in ('WIN','LOSS')]
    if not rows:return {'samples':0,'bias':0.0,'brier':0.0,'status':'NO DATA'}
    errs=[];bias=[]
    for x in rows:
        p=max(0,min(1,_f(x.get('confidence'),50)/100));y=1 if _s(x.get('result') or x.get('status'))=='WIN' else 0
        errs.append((p-y)**2);bias.append((y-p)*100)
    b=sum(errs)/len(errs);adj=max(-10,min(10,sum(bias)/len(bias)))
    state['confidence_calibration_v107']={'samples':len(rows),'bias':round(adj,2),'brier':round(b,4),'updated_at':time.time()}
    return {'samples':len(rows),'bias':round(adj,2),'brier':round(b,4),'status':'GOOD' if b<=.12 else 'WATCH' if b<=.22 else 'POOR'}

def signal_lifecycle(state):
    life=dict(state.get('signal_lifecycle_v107') or {});now=time.time();created=updated=closed=0
    for key in ('paper_positions','shadow_positions','signals','shadow_signals'):
        for r in state.get(key) or []:
            if not isinstance(r,dict):continue
            sid=str(r.get('id') or r.get('signal_id') or r.get('trade_id') or '')
            if not sid:continue
            status=_s(r.get('status') or r.get('result') or 'OPEN');stage='CLOSED' if status in ('WIN','LOSS','TP','SL','TIMEOUT','CLOSED') else 'ACTIVE'
            if sid not in life:
                life[sid]={'id':sid,'symbol':_s(r.get('symbol') or r.get('ticker')),'side':_s(r.get('side') or r.get('direction')),'created_at':now,'stage':stage,'updates':1};created+=1
            else:
                if life[sid].get('stage')!='CLOSED' and stage=='CLOSED':closed+=1
                life[sid]['stage']=stage;life[sid]['updates']=int(life[sid].get('updates',0))+1;life[sid]['updated_at']=now;updated+=1
    state['signal_lifecycle_v107']=life
    c=Counter(x.get('stage') for x in life.values())
    return {'total':len(life),'created':created,'updated':updated,'closed_now':closed,'active':c.get('ACTIVE',0),'closed':c.get('CLOSED',0)}

def strategy_benchmark(state):
    groups=defaultdict(list)
    for k in ('shadow_learning_v105','experience_bank_v104'):
        for x in state.get(k) or []:
            result=_s(x.get('result') or x.get('status'))
            if result not in ('WIN','LOSS'):continue
            st=_s(x.get('strategy') or x.get('signal_type') or 'UNCLASSIFIED')
            groups[st].append(1 if result=='WIN' else 0)
    rows=[{'strategy':k,'samples':len(v),'win_rate':round(sum(v)/len(v)*100,1)} for k,v in groups.items()]
    rows.sort(key=lambda x:(x['samples'],x['win_rate']),reverse=True)
    state['strategy_benchmark_v107']=rows
    return {'strategies':len(rows),'rows':rows[:10],'best':rows[0]['strategy'] if rows else 'NO DATA'}

def ai_scorecard(state, accuracy=None):
    exp=len(state.get('experience_bank_v104') or [])+len(state.get('shadow_learning_v105') or [])
    dna=len(state.get('mtf_dna_v105') or [])+len(state.get('global_dna_v105') or [])+len(state.get('master_dna_v104') or [])
    coverage=len({x.get('symbol') for x in state.get('autonomous_market_scans_v107',[]) if x.get('symbol')})
    acc=accuracy or {};actual=_f(acc.get('actual'));mae=_f(acc.get('mae'),100)
    learning=min(100,exp*.5+dna*2);stability=max(0,100-mae*2);score=learning*.3+actual*.3+min(100,coverage*10)*.2+stability*.2
    return {'score':round(score,1),'level':1+int(score//20),'experience':exp,'dna':dna,'accuracy':actual,'coverage':coverage,'stability':round(stability,1)}

def autonomous_cycle(state, detector, accuracy):
    scan=auto_market_scan(state);reg=regime_history(state,detector);cal=confidence_calibration(state);life=signal_lifecycle(state);bench=strategy_benchmark(state);card=ai_scorecard(state,accuracy(state))
    state['autonomous_scheduler_v107']={'enabled':True,'last_run':time.time(),'interval_minutes':15,'runs':int((state.get('autonomous_scheduler_v107') or {}).get('runs',0))+1}
    return {'scan':scan,'regime':reg,'calibration':cal,'lifecycle':life,'benchmark':bench,'scorecard':card,'scheduler':state['autonomous_scheduler_v107'],'advisory_only':True}
