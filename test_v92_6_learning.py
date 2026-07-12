from __future__ import annotations
import importlib.util, os, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('TELEGRAM_BOT_TOKEN','')
os.environ.setdefault('TELEGRAM_CHAT_ID','')
os.environ.setdefault('COINGLASS_API_KEY','')
os.environ.setdefault('DATABASE_URL','')
for k in ('PAPER_MAX_POSITIONS','PAPER_MAX_LONG_POSITIONS','PAPER_MAX_SHORT_POSITIONS','PAPER_SHADOW_MAX_POSITIONS','PAPER_SHADOW_COOLDOWN_MINUTES','PAPER_SHADOW_CAPTURE_TOP','PAPER_CANDIDATE_LIMIT','PAPER_LEARNING_INCLUDE_SHADOW','A100_LEARNING_TARGET_SAMPLES'):
    os.environ.pop(k,None)
with tempfile.TemporaryDirectory(prefix='a100_v926_') as tmp:
    os.environ['A100_DATA_DIR']=tmp
    spec=importlib.util.spec_from_file_location('a100_v926',ROOT/'main.py')
    module=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(module)
    assert module.V91_VERSION.startswith('A100 V92.6')
    assert module._v91_default_state()['schema']==1
    assert module.V91_STATE_FILE.endswith('a100_v91_paper_state.json')
    assert module.V91_MAX_POSITIONS==20
    assert module.V912_MAX_LONG==12 and module.V912_MAX_SHORT==12
    assert module.V914_SHADOW_MAX==60 and module.V914_SHADOW_CAPTURE_TOP==60
    assert module.V914_SHADOW_COOLDOWN_MIN==5 and module.V914_LEARNING_INCLUDE_SHADOW is True
    assert module.V912_CANDIDATE_LIMIT==60 and module.V912_SCAN_SECONDS==120
    assert module.V925_LEARNING_TARGET_SAMPLES==150
    for cmd in ('intelligence','decisionai','learningstatus','learningreport','dashboard','final','help','commands'):
        assert callable(module.V90_COMMAND_REGISTRY[cmd])
    assert module._v926_stage_weight('WATCH') < module._v926_stage_weight('READY') < module._v926_stage_weight('ENTRY')
    text=module._v926_learning_report_text(False)
    assert 'A100 V92.6' in text and 'Shadow OPEN' in text and '최근 24시간' in text
    pre=module.v91_preflight(); assert pre['ok'],pre
print('A100 V92.6 learning/sampling regression test: PASS')
