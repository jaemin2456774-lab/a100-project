from pathlib import Path
import ast

SOURCE = Path(__file__).with_name('main.py').read_text()
TREE = ast.parse(SOURCE)


def test_builder_uses_frozen_base_alias():
    funcs = {n.name: n for n in TREE.body if isinstance(n, ast.FunctionDef)}
    fn = funcs['_v1160_s21729_build_live_state']
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    names = {n.func.id for n in calls}
    assert '_v1160_s21728_build_live_state_base' in names
    assert '_v1160_s21728_build_live_state' not in names


def test_base_alias_precedes_public_rebind():
    alias = SOURCE.index('_v1160_s21728_build_live_state_base = _v1160_s21728_build_live_state')
    rebind = SOURCE.index('_v1160_s21728_build_live_state = _v1160_s21729_build_live_state')
    assert alias < rebind


def test_hotfix_version_and_invariants():
    assert '116.0-LTS-S2.17.29.1' in SOURCE
    assert 'V90_EXPECTED_COMMANDS=frozenset(V90_COMMAND_REGISTRY)' in SOURCE
    assert "'releasegate':releasegate1160ltss21729_cmd" in SOURCE
