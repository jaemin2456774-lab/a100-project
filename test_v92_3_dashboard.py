import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('a100_v923', HERE/'main.py')
m=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(m)

assert len(m.V90_COMMAND_REGISTRY)>=150, len(m.V90_COMMAND_REGISTRY)
for cmd in ('dashboard','final','coach','topscore','help','commands'):
    assert callable(m.V90_COMMAND_REGISTRY.get(cmd)), cmd
for alias,target in m.V922_ALIASES.items():
    assert m.V90_COMMAND_REGISTRY[alias] is m.V90_COMMAND_REGISTRY[target], (alias,target)
audit=m._v923_help_audit()
assert not audit['usage_missing'], audit
assert not audit['category_missing'], audit
assert not audit['aliases_bad'], audit
sample={'symbol':'BTCUSDT','side':'LONG','score':92.0,'grade':'S','confidence':88.0,'stage':'ENTRY','meta_decision':'TRADE','risk_mode':'NORMAL','components':{'Risk':85}}
gate={'passed':True,'status':'TRADE','reasons':[]}
assert m._v923_compact_action(sample,gate,{})=='BUY NOW'
assert m._v923_risk_label(sample,gate)=='LOW'
assert m._v923_coach_plan(sample,gate,{'entry_low':1,'entry_high':2})[0]=='소액 분할진입 검토'
pre=m.v91_preflight()
for key in ('v923_command_count','v923_callbacks','v923_aliases','v923_help_sync','v923_live_trading_disabled'):
    assert pre['checks'][key], (key,pre['checks'])
assert pre['data_compatibility']['schema']==1
print('V92.3 tests PASS',len(m.V90_COMMAND_REGISTRY))
