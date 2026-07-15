from pathlib import Path
import ast

p = Path(__file__).with_name('main.py')
s = p.read_text(encoding='utf-8')
ast.parse(s)
# S2.17.27 remains the architectural recovery milestone, superseded by
# S2.17.28 monitoring stabilization without reverting to snapshot-first.
assert 'Runtime recovery: S2.17.27' in s
assert 'Worker → Live Runtime State → Telegram Strict Read Only' in s
assert 'Snapshot      Certification / Recovery Evidence' in s
assert s.count('if __name__ == "__main__":') == 1
print('S2.17.27 architecture continuity regression: PASS')
