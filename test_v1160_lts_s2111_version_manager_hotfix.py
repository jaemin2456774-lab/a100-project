import ast
from pathlib import Path

P = Path(__file__).with_name("main.py")
S = P.read_text(encoding="utf-8")
T = ast.parse(S)


def test_python_syntax():
    assert isinstance(T, ast.Module)


def test_version_manager_uses_defined_class():
    assert "V1160_VERSION_MANAGER = _V1160RC4923VersionManager(" in S
    assert "V1160_VERSION_MANAGER = V1160VersionManager(" not in S


def test_manager_constructor_has_supported_fields_only():
    target = None
    for node in ast.walk(T):
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "V1160_VERSION_MANAGER" for t in node.targets):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "_V1160RC4923VersionManager":
                    if any(k.arg == "number" for k in node.value.keywords) and any(k.arg == "version" for k in node.value.keywords):
                        target = node.value
    assert target is not None
    assert {k.arg for k in target.keywords} <= {"number", "version", "schema", "paper", "shadow", "live", "source"}


def test_lts_policy_guards_preserved():
    assert 'V1160_LTS_S211_NUMBER = "116.0-LTS-S2.11"' in S
    assert 'V91_MAX_POSITIONS==20 and V914_SHADOW_MAX==60' in S
    assert '"s211_live_off"' in S
    assert 'len(V90_COMMAND_REGISTRY)==341' in S
