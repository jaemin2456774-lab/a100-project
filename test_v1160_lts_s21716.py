from pathlib import Path
p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
assert 'V1160_LTS_S21716_VERSION' in s
assert 'RUNTIME SCORE COMPOSITION V5' in s
assert 'EVIDENCE COVERAGE ANALYZER' in s
assert 'MANDATORY GATE EXPLAIN ENGINE V3' in s
assert 'LTS CERTIFICATION PROGRESS' in s
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
print('S2.17.16 static regression PASS')
