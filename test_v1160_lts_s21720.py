from pathlib import Path
import py_compile

p=Path('main.py')
text=p.read_text(encoding='utf-8')
py_compile.compile(str(p),doraise=True)
assert '116.0-LTS-S2.17.20' in text
assert 'STRATEGY TRUST EVIDENCE ENGINE V3' in text
assert 'EVIDENCE CORRELATION V4 · QUALITY AWARE' in text
assert 'RUNTIME SCORE COMPOSITION V9 · EVIDENCE VERIFIED' in text
assert 'MANDATORY GATE FORECAST V7 · AUTHORITATIVE' in text
assert 'PRODUCTION READINESS DASHBOARD V5 · VERIFIED' in text
assert text.count('if __name__ == "__main__":') == 1
assert text.rstrip().endswith('main()')
print('S2.17.20 static regression: PASS')
