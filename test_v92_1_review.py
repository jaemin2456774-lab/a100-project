import importlib.util, os, tempfile, time

spec=importlib.util.spec_from_file_location('a100_main','main.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def item(score=90, confidence=85, stage='ENTRY', market=80):
    return {'symbol':'BTCUSDT','side':'LONG','score':score,'grade':'S','confidence':confidence,'stage':stage,
            'meta_decision':'TRADE','risk_mode':'NORMAL','components':{'Pattern':80,'Liquidity':80,'Momentum':80,'Market':market,'Risk':80,'Timing':80,'Learning':80,'Meta':80},
            'positives':['test'],'risks':[]}

assert m._v921_precision_gate(item())['passed']
assert not m._v921_precision_gate(item(score=70))['passed']
assert not m._v921_precision_gate(item(market=30))['passed']

with tempfile.TemporaryDirectory() as d:
    m.V91_STATE_FILE=os.path.join(d,'a100_v91_paper_state.json')
    now=1_700_000_000.0
    row,created=m._v921_record_audit(item(),now=now,price=100.0)
    assert created and row['status']=='OPEN'
    row2,created2=m._v921_record_audit(item(),now=now+60,price=100.0)
    assert not created2 and row2['id']==row['id']
    reviewed,state=m._v921_review_due(now=now+m.V921_REVIEW_HOURS*3600+1,prices={'BTCUSDT':102.0})
    assert len(reviewed)==1 and reviewed[0]['outcome']=='WIN'
    stats=m._v921_memory_stats(state)
    assert stats['all']['n']==1 and stats['all']['w']==1 and stats['precision']['wr']==100.0
    loaded=m._v91_load_state()
    assert loaded['schema']==1 and len(loaded['decision_audits'])==1

pre=m.v91_preflight()
assert pre['ok'], [k for k,v in pre['checks'].items() if not v]
assert pre['command_count']>=141
assert not pre['help_audit']['usage_missing'] and not pre['help_audit']['stale_usage']
print('V92.1 PASS')
