from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parent
SRC=(ROOT/'main.py').read_text(encoding='utf-8')
ast.parse(SRC)
assert SRC.count('if __name__ == "__main__":') == 1
assert 'V1160_LTS_S21746_NUMBER = "116.0-LTS-S2.17.46"' in SRC
assert 'FINAL CERTIFICATION INTELLIGENCE & RELEASE VIEW' in SRC
for token in (
    '_v1160_s21746_gate_rows','_v1160_s21746_trend','_v1160_s21746_eta',
    '_v1160_s21746_release_view','_v1160_s21746_final_lines',
    'evidence1160ltss21746_cmd','ltsreadiness1160ltss21746_cmd',
    'runtimehealth1160ltss21746_cmd','coach1160ltss21746_cmd',
    'Registry remains 341','Gate formulas unchanged','Live OFF'):
    assert token in SRC, token
assert SRC.rstrip().endswith('main()')
print('S2.17.46 static regression PASS')
