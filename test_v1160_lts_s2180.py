from pathlib import Path
import ast, re
p=Path(__file__).with_name('main.py')
s=p.read_text()
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
start=s.rfind('# A100 V116.0-LTS-S2.18.0')
end=s.find('# A100 V116.0-LTS-S2.18.1', start)
segment=s[start:end if end!=-1 else None]
for token in [
    'V1160_LTS_S2180_NUMBER','_V1160S2180RuntimeState','_V1160S2180Evidence',
    '_V1160S2180Formatter','_v1160_s2180_build_state','_v1160_s2180_operational_preflight',
    'version1160ltss2180_cmd','versionaudit1160ltss2180_cmd','status1160ltss2180_cmd',
    'runtimehealth1160ltss2180_cmd','releasegate1160ltss2180_cmd',
    'ltscertification1160ltss2180_cmd','pipelinetrace1160ltss2180_cmd'
]:
    assert token in segment, token
for mapping in [
    "'version':version1160ltss2180_cmd",
    "'versionaudit':versionaudit1160ltss2180_cmd",
    "'status':status1160ltss2180_cmd",
    "'runtimehealth':runtimehealth1160ltss2180_cmd",
    "'releasegate':releasegate1160ltss2180_cmd",
    "'ltscertification':ltscertification1160ltss2180_cmd",
    "'pipelinetrace':pipelinetrace1160ltss2180_cmd",
]:
    assert mapping in segment, mapping
rg=re.search(r'async def releasegate1160ltss2180_cmd.*?async def ltscertification1160ltss2180_cmd',segment,re.S).group(0)
assert 'create_task' not in rg
assert '_v1160_s2173_cached_snapshot' not in segment
assert segment.count('_v1160_s21724_gate_matrix(snap, detail)') == 1
assert "V90_EXPECTED_COMMANDS=frozenset(V90_COMMAND_REGISTRY)" in segment
print('S2.18.0 unified runtime state static regression: PASS')
