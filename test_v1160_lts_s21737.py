from pathlib import Path
import ast

src = Path('main.py').read_text(encoding='utf-8')
ast.parse(src)
assert 'V1160_LTS_S21737_NUMBER = "116.0-LTS-S2.17.37"' in src
assert 'V91_VERSION = V1160_LTS_S21737_VERSION' in src
assert "'versionaudit': versionaudit1160ltss21737_cmd" in src
assert "'version': version1160ltss21737_cmd" in src
assert "Registry/Callable/Expected 341" in src
assert 'Gate formulas UNCHANGED · no Telegram recomputation' in src
assert src.rstrip().endswith('main()')
assert src.count('if __name__ == "__main__":') == 1
print('S2.17.37 regression PASS')
