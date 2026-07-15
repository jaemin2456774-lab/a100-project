from pathlib import Path
import ast, re
p=Path(__file__).with_name('main.py')
s=p.read_text()
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
for token in ['V1160_LTS_S21729_NUMBER','_v1160_s21729_operational_preflight','version1160ltss21729_cmd','versionaudit1160ltss21729_cmd','runtimehealth1160ltss21729_cmd','releasegate1160ltss21729_cmd']:
    assert token in s, token
assert 'V1160_VERSION_MANAGER = _V1160RC4923VersionManager(' in s
segment=s[s.rfind('# A100 V116.0-LTS-S2.17.29'):]
assert not re.search(r'V1160_VERSION_MANAGER\.(number|version)\s*=(?!=)', segment)
assert "'version':version1160ltss21729_cmd" in segment
assert "'versionaudit':versionaudit1160ltss21729_cmd" in segment
assert "'runtimehealth':runtimehealth1160ltss21729_cmd" in segment
assert "'releasegate':releasegate1160ltss21729_cmd" in segment
assert "create_task" not in re.search(r'async def releasegate1160ltss21729_cmd.*?async def versionaudit1160ltss21729_cmd', segment, re.S).group(0)
print('S2.17.29 clean stabilization static regression: PASS')
