from pathlib import Path
import ast,re
s=Path('main.py').read_text()
assert 'V1160_LTS_S21727_NUMBER = "116.0-LTS-S2.17.27"' in s
assert "'runtimehealth': runtimehealth1160ltss21727_cmd" in s
assert "'releasegate': releasegate1160ltss21727_cmd" in s
assert "'version': version1160ltss21727_cmd" in s
assert 'create_task' not in re.search(r'async def releasegate1160ltss21727_cmd.*?\n\ndef ',s,re.S).group(0)
rt=re.search(r'async def runtimehealth1160ltss21727_cmd.*?\n\nasync def ',s,re.S).group(0)
assert '_v91_load_state' not in rt
assert '_v1160_s21_runtime_view' not in rt
ast.parse(s)
print('S2.17.27 static regression tests: PASS')
