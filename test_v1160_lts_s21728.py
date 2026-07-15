from pathlib import Path
import ast,re
s=Path('main.py').read_text(encoding='utf-8')
assert 'V1160_LTS_S21728_NUMBER = "116.0-LTS-S2.17.28"' in s
assert '_V1160_S21728_REPLY_ROOT = globals().get(\'_V1160_S21725_SAFE_REPLY_BASE\'' in s
assert "'versionaudit': versionaudit1160ltss21728_cmd" in s
assert "'runtimehealth': runtimehealth1160ltss21728_cmd" in s
assert "'releasegate': releasegate1160ltss21728_cmd" in s
assert s.rstrip().endswith('main()')
# final wrapper must call root directly, never the S2.17.27 or S2.17.25 wrapper.
block=re.search(r'async def v90_1_safe_reply\(update, value, \*args, \*\*kwargs\):.*?\n\n',s[s.index('# A100 V116.0-LTS-S2.17.28'):],re.S).group(0)
assert '_V1160_S21728_REPLY_ROOT' in block
assert '_V1160_S21727_SAFE_REPLY_BASE' not in block
# active version audit must use the active preflight.
audit=re.search(r'async def versionaudit1160ltss21728_cmd.*?\n\n\n',s,re.S).group(0)
assert '_v1160_s21728_light_preflight' in audit
ast.parse(s)
print('S2.17.28 static regression tests: PASS')
