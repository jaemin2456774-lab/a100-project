from pathlib import Path
import ast
p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
ast.parse(s)
assert 'V1160_LTS_S21745_NUMBER = "116.0-LTS-S2.17.45"' in s
assert "_v1160_s2176_check('Registry remains 341',len(V90_COMMAND_REGISTRY)==341)" in s
assert 'All maturity scores are DISPLAY ONLY.' in s
assert 'No storage scan · no rebuild · no gate recomputation.' in s
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
print('S2.17.45 static regression PASS')
