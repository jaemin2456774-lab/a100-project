from pathlib import Path
import ast

src=Path('main.py').read_text(encoding='utf-8')
ast.parse(src)
assert '116.0-LTS-S2.17.18' in src
assert 'RUNTIME SCORE COMPOSITION V7' in src
assert 'EVIDENCE COVERAGE PREDICTOR V3' in src
assert 'MANDATORY GATE STATUS V5' in src
assert 'PRODUCTION READINESS DASHBOARD V3' in src
assert src.count('if __name__ == "__main__":') == 1
assert src.rstrip().endswith('main()')
print('S2.17.18 static regression PASS')
