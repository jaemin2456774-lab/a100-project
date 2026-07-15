from pathlib import Path
p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
assert '116.0-LTS-S2.17.2' in s
assert '_A100_HEALTH_SERVER_LOCK' in s
assert '_A100_HEALTH_SERVER_STARTED' in s
assert 'Address already in use' not in s
assert '_v1160_s2172_gate_diagnostic' in s
assert s.count('if __name__ == "__main__":') == 1
print('S2.17.2 static checks PASS')
