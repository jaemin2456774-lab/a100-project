import ast
from pathlib import Path

SRC=Path(__file__).with_name('main.py')
TEXT=SRC.read_text(encoding='utf-8')
TREE=ast.parse(TEXT)

def test_syntax_and_version():
    assert TREE is not None
    assert 'V1160_LTS_S212_NUMBER = "116.0-LTS-S2.12"' in TEXT
    assert 'SCORE CALIBRATION & FORECAST' in TEXT

def test_routes_preserved():
    assert 'len(V90_COMMAND_REGISTRY)==341' in TEXT
    for cmd in ('version','status','runtimehealth','dashboard','releasegate'):
        assert f'"{cmd}":' in TEXT

def test_policy_preserved():
    assert 'V91_MAX_POSITIONS==20' in TEXT
    assert 'V914_SHADOW_MAX==60' in TEXT
    assert 'place_live_order' in TEXT and 'submit_live_order' in TEXT

def test_authoritative_gate_notice():
    assert 'Mandatory gates remain authoritative' in TEXT
    assert '_v1160_s212_authoritative_evidence' in TEXT
    assert '_v1160_s212_runtime_intelligence' in TEXT
