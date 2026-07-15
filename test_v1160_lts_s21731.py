from pathlib import Path
p=Path(__file__).with_name('main.py').read_text(encoding='utf-8')
assert '116.0-LTS-S2.17.31' in p or '116.0-LTS-S2.17.32' in p or '116.0-LTS-S2.17.33' in p
assert 'LTS FINAL UNIFIED DASHBOARD & GAUGE POLISH' in p or 'LTS FINAL VISUAL GAUGE CONSISTENCY POLISH' in p or 'LTS FINAL OPERATIONS CONSOLE POLISH' in p
assert 'def _v1160_s21731_certification_milestones' in p
assert 'async def dashboard1160ltss21731_cmd' in p
assert "'dashboard':dashboard1160ltss21731_cmd" in p or "'dashboard':dashboard1160ltss21732_cmd" in p or "'dashboard':dashboard1160ltss21733_cmd" in p
assert "_v1160_s2176_check('Unified live dashboard'" in p
assert 'CERTIFICATION MILESTONES' in p
assert "for hours in (1,6,12,24,48,72)" in p
assert 'Telegram path        STRICT READ ONLY' in p
assert p.count('if __name__ == "__main__":') == 1
# The active dashboard and certification views must only read the live memory state.
for name in ('dashboard1160ltss21731_cmd','ltscertification1160ltss21730_cmd','status1160ltss21730_cmd','releasegate1160ltss21730_cmd'):
    start=p.index(f'async def {name}')
    end=p.find('\nasync def ',start+10)
    if end < 0: end=len(p)
    body=p[start:end]
    assert '_v1160_s21728_read_live_state()' in body
    assert '_v1160_s21726_fast_context' not in body
    assert '_v1160_s21724_gate_matrix' not in body
print('PASS S2.17.31')
