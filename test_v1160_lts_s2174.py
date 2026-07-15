from pathlib import Path
p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
assert 'V1160_LTS_S2174_NUMBER = "116.0-LTS-S2.17.4"' in s
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
assert 'def _v1160_s2174_light_preflight' in s
assert 'def build_v44_application(token):' in s
assert 'releasegate1160ltss2173_cmd' in s
print('S2.17.4 static tests: PASS')
