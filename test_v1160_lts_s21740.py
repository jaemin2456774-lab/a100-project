from pathlib import Path
import ast
p=Path('main.py')
s=p.read_text()
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
required=[
 'V1160_LTS_S21740_NUMBER = "116.0-LTS-S2.17.40"',
 'async def version1160ltss21740_cmd',
 'async def versionaudit1160ltss21740_cmd',
 'async def commandcert1160ltss21740_cmd',
 'async def runtimehealth1160ltss21740_cmd',
 'def _v1160_s21740_summary_lines',
 'def _v1160_s21740_reconcile_handlers',
 'def _v1160_s21740_light_preflight',
 'Success Rate',
 'Release Freeze                  ACTIVE',
 '🛡️ Version Audit',
 '🧾 Command Cert',
 '🔗 Pipeline',
 'A100 S2.17.40 live runtime worker: ACTIVE',
]
for token in required:
    assert token in s, token
last=s.rsplit('def main():',1)[1]
assert '_v1160_s21740_light_preflight(True)' in last
assert 'S2.17.38 bounded startup preflight failed' not in last
assert "'version':version1160ltss21740_cmd" in s
assert "'versionaudit':versionaudit1160ltss21740_cmd" in s
assert "'commandcert':commandcert1160ltss21740_cmd" in s
assert "'runtimehealth':runtimehealth1160ltss21740_cmd" in s
print('S2.17.40 static regression PASS')
