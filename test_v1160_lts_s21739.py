from pathlib import Path
import ast
p=Path('main.py')
s=p.read_text()
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
for token in [
    'V1160_LTS_S21739_NUMBER = "116.0-LTS-S2.17.39"',
    'async def version1160ltss21739_cmd',
    'async def versionaudit1160ltss21739_cmd',
    'def _v1160_s21739_reconcile_handlers()',
    "'S2.17.37 version audit handler active'",
    "'S2.17.37 version handler active'",
    'A100 S2.17.39 startup auto-recovered routes:',
    'S2.17.39 unrecoverable startup preflight failed',
    "'version': version1160ltss21739_cmd",
]:
    assert token in s, token
# The current main must not use the S2.17.38 bounded fail message.
last = s.rsplit('def main():', 1)[1]
assert 'S2.17.38 bounded startup preflight failed' not in last
assert "_v1160_s21739_light_preflight(True)" in last
print('S2.17.39 static regression PASS')
