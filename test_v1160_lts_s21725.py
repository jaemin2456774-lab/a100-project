from pathlib import Path
import ast

SRC=Path(__file__).with_name('main.py').read_text(encoding='utf-8')
ast.parse(SRC)
assert '116.0-LTS-S2.17.25' in SRC
assert 'FINAL GATE DIAGNOSTICS & VERSION SOURCE UNIFICATION' in SRC
assert 'def _v1160_s21725_snapshot_key(snap):' in SRC
assert 'V1160_S21725_SCORE_CACHE' in SRC
assert 'def _v1160_s21725_normalize_version_text(value):' in SRC
assert "BLOCKED/EVIDENCE" in SRC and "BLOCKED/SCORE" in SRC
assert 'Gate {idx} · {item[\'label\']}' in SRC
assert 'Score is read from the active production Strategy Trust engine' in SRC
assert 'No forecast, display state or synthetic uplift is counted.' in SRC
assert "'strategytrust':strategytrust1160ltss21725_cmd" in SRC
assert "'outcomequality':outcomequality1160ltss21725_cmd" in SRC
assert "'releasegate':releasegate1160ltss21725_cmd" in SRC
assert "'versionaudit':versionaudit1160ltss21725_cmd" in SRC
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')
print('S2.17.25 regression tests: PASS')
