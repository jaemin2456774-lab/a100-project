from pathlib import Path
import ast

p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
ast.parse(s)
assert s.count('if __name__ == "__main__"') == 1
assert s.rstrip().endswith('main()')
for token in (
    '116.0-LTS-S2.17.15',
    'RUNTIME EVIDENCE CORRELATION V3',
    'RUNTIME WINDOW ENGINE V3 · UNIFIED SOURCE',
    'UNIFIED CACHE / BUILD METRICS V3',
    'RUNTIME EVIDENCE CONSISTENCY AUDIT',
    'Canonical evidence source',
    'Window subset monotonic',
    'Cache arithmetic',
):
    assert token in s, token
assert 'V90_COMMAND_REGISTRY.update({"version":version1160ltss21715_cmd' in s
print('S2.17.15 static regression: PASS')
