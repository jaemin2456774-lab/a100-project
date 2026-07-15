from pathlib import Path
import ast, re
src=Path('main.py').read_text()
ast.parse(src)
assert 'A100 S2.17.28 bounded startup preflight failed' not in src[src.rfind('# A100 V116.0-LTS-S2.17.28.1'):]
assert "startup_ok" in src
assert "certification preflight findings" in src
assert "operational startup preflight failed" in src
assert "V1160_LTS_S217281_NUMBER = \"116.0-LTS-S2.17.28.1\"" in src
assert src.count('if __name__ == "__main__":') == 1
print('S2.17.28.1 static regression: PASS')
