from pathlib import Path
s=Path('main.py').read_text()
assert '116.0-LTS-S2.17.12' in s
assert 'RUNTIME EVIDENCE DATABASE' in s
assert '_v1160_s21712_start_scheduler_once' in s
assert s.count('if __name__ == "__main__"') == 1
assert s.rstrip().endswith('main()')
print('S2.17.12 static checks: PASS')
