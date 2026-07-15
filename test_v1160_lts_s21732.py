from pathlib import Path
p=Path('main.py').read_text()
assert '116.0-LTS-S2.17.32' in p or '116.0-LTS-S2.17.33' in p
assert 'LTS FINAL VISUAL GAUGE CONSISTENCY POLISH' in p or 'LTS FINAL OPERATIONS CONSOLE POLISH' in p
for group in [
    ('def _v1160_s21732_gate_lines','def _v1160_s21733_gate_lines'),
    ('def _v1160_s21732_summary_lines','def _v1160_s21733_summary_lines'),
    ('async def status1160ltss21732_cmd','async def status1160ltss21733_cmd'),
    ('async def releasegate1160ltss21732_cmd','async def releasegate1160ltss21733_cmd'),
    ('async def dashboard1160ltss21732_cmd','async def dashboard1160ltss21733_cmd'),
    ('async def ltscertification1160ltss21732_cmd','async def ltscertification1160ltss21733_cmd'),
]:
    assert any(token in p for token in group), group
assert 'Telegram path STRICT READ ONLY' in p
assert 'Snapshot SUPPORTING EVIDENCE ONLY' in p
assert "'status':status1160ltss21732_cmd" in p or "'status':status1160ltss21733_cmd" in p
assert "'releasegate':releasegate1160ltss21732_cmd" in p or "'releasegate':releasegate1160ltss21733_cmd" in p
assert "'dashboard':dashboard1160ltss21732_cmd" in p or "'dashboard':dashboard1160ltss21733_cmd" in p
assert "'ltscertification':ltscertification1160ltss21732_cmd" in p or "'ltscertification':ltscertification1160ltss21733_cmd" in p
assert p.count('if __name__ == "__main__":') == 1
print('PASS S2.17.32 visual gauge compatibility')
