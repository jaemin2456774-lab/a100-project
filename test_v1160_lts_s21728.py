from pathlib import Path
import ast

p = Path(__file__).with_name('main.py')
s = p.read_text(encoding='utf-8')
tree = ast.parse(s)
assert '116.0-LTS-S2.17.28' in s
assert 'REAL-TIME MONITORING STABILIZATION' in s
assert "V1160_S21728_LIVE_INTERVAL = 2.0" in s
assert "V1160_S21728_EVIDENCE_INTERVAL = 30.0" in s
assert "a100-s21728-live-runtime" in s
assert "Command calculation  DISABLED" in s
assert "Telegram performs no gate, evidence, file, or snapshot calculation." in s
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')

funcs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
for name in (
    'status1160ltss21728_cmd',
    'runtimehealth1160ltss21728_cmd',
    'releasegate1160ltss21728_cmd',
):
    node = funcs[name]
    called = {
        sub.func.id
        for sub in ast.walk(node)
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
    }
    assert '_v1160_s21726_fast_context' not in called, (name, called)
    assert '_v1160_s21724_gate_matrix' not in called, (name, called)
    assert '_v1160_s21728_read_live_state' in called, (name, called)

start = funcs['_v1160_s21728_start_live_worker_once']
globals_declared = {
    name
    for sub in start.body
    if isinstance(sub, ast.Global)
    for name in sub.names
}
assert 'V1160_S21728_LIVE_THREAD' in globals_declared
assert 'V1160_S21728_LIVE_STARTED' in globals_declared

assert "'status': status1160ltss21728_cmd" in s
assert "'runtimehealth': runtimehealth1160ltss21728_cmd" in s
assert "'releasegate': releasegate1160ltss21728_cmd" in s
assert "'versionaudit': versionaudit1160ltss21728_cmd" in s
print('S2.17.28 real-time monitoring stabilization regression: PASS')
