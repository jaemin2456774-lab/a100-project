from pathlib import Path
import ast
p=Path(__file__).with_name('main.py')
s=p.read_text()
assert 'V1160_LTS_S2181_NUMBER = "116.0-LTS-S2.18.1"' in s
assert 'def _v1160_s2181_build_state' in s
assert "'hits': 0, 'misses': 0, 'prewarmed': False" in s
assert 'Gate calculation     ONCE PER SNAPSHOT' in s
assert 'Recalculation        DISABLED FOR SAME SNAPSHOT' in s
assert 'A100 S2.18.1 unified state prewarm' in s
assert "'version':version1160ltss2181_cmd" in s
assert "'runtimehealth':runtimehealth1160ltss2181_cmd" in s
assert "'releasegate':releasegate1160ltss2181_cmd" in s
ast.parse(s)
print('S2.18.1 static regression: PASS')
