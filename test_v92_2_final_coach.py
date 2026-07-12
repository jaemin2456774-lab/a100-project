import importlib.util, os, tempfile, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('a100_v922', HERE/'main.py')
m=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(m)

assert len(m.V90_COMMAND_REGISTRY)==149, len(m.V90_COMMAND_REGISTRY)
for cmd in ('final','coach','confidence_history','paper','shadow','market','meta','ev','ai'):
    assert callable(m.V90_COMMAND_REGISTRY.get(cmd)), cmd
for alias,target in m.V922_ALIASES.items():
    assert m.V90_COMMAND_REGISTRY[alias] is m.V90_COMMAND_REGISTRY[target], (alias,target)
assert not m._v922_help_audit()['usage_missing']

sample={
 'symbol':'BTCUSDT','side':'LONG','score':92.0,'grade':'S','confidence':88.0,'stage':'ENTRY','meta_decision':'TRADE','risk_mode':'NORMAL',
 'components':{'Pattern':82,'Liquidity':80,'Momentum':78,'Market':75,'Risk':85,'Timing':88,'Learning':70,'Meta':84},
 'positives':['ok'],'risks':[]
}
gate=m._v921_precision_gate(sample)
assert gate['passed'], gate
assert m._v922_position_pct(sample,gate)>0
assert '진입' in m._v922_action(sample,gate,{})

with tempfile.TemporaryDirectory() as td:
    old=m.V91_STATE_FILE
    m.V91_STATE_FILE=os.path.join(td,'a100_v91_paper_state.json')
    try:
        st=m._v91_default_state(); m._v91_save_state(st)
        row,new=m._v922_record_confidence(sample,'test')
        assert new and row['symbol']=='BTCUSDT'
        row2,new2=m._v922_record_confidence(sample,'test')
        assert not new2
        state=m._v91_load_state()
        assert state.get('schema')==1
        assert len(state.get('confidence_history',[]))==1
    finally:
        m.V91_STATE_FILE=old

pre=m.v91_preflight()
assert pre['checks']['v922_command_count']
assert pre['checks']['v922_aliases']
assert pre['checks']['v922_help_sync']
assert pre['checks']['v922_live_trading_disabled']
print('V92.2 tests PASS', len(m.V90_COMMAND_REGISTRY))
