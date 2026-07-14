from pathlib import Path
import ast

p = Path(__file__).with_name('main.py')
s = p.read_text(encoding='utf-8')
ast.parse(s)

assert s.count('if __name__ == "__main__":') == 1
assert s.rfind('if __name__ == "__main__":') > s.find('async def version1160ltss212_cmd')
assert s.rfind('if __name__ == "__main__":') > s.find('def v91_preflight(force=False):', 44900)
assert 'V1160_LTS_S212_NUMBER = "116.0-LTS-S2.13"' in s
assert 'A100 V116.0-LTS-S2.13 FINAL CALIBRATION ACTIVATION' in s
assert 'Raw / calibrated' in s
assert 'Mandatory gates remain authoritative' in s
assert 'V90_COMMAND_REGISTRY.update({"version":version1160ltss212_cmd' in s
assert 'V116.0 LTS-S2.13 startup integrity failure' in s
print('PASS: 8/8 activation and static regression checks')
