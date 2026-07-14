import ast
from pathlib import Path

P=Path(__file__).with_name("main.py")
S=P.read_text(encoding="utf-8")
T=ast.parse(S)

def test_syntax_and_final_block():
    assert isinstance(T, ast.Module)
    assert S.rstrip().endswith("_v1160_rc45_start_worker(); main()")

def test_version_and_handlers():
    assert 'V1160_LTS_S211_NUMBER = "116.0-LTS-S2.11"' in S
    for name in ("version1160ltss211_cmd","status1160ltss211_cmd","runtimehealth1160ltss211_cmd","dashboard1160ltss211_cmd","releasegate1160ltss211_cmd"):
        assert f"async def {name}" in S

def test_final_polish_engines():
    for name in ("_v1160_s211_gate_forecast","_v1160_s211_learning_intelligence","_v1160_s211_evidence_timeline","_v1160_s211_runtime_intelligence","_v1160_s211_memory_intelligence"):
        assert f"def {name}" in S

def test_policy_guards():
    assert '"s211_registry_341":len(V90_COMMAND_REGISTRY)==341' in S
    assert 'V91_MAX_POSITIONS==20 and V914_SHADOW_MAX==60' in S
    assert '"s211_live_off"' in S
