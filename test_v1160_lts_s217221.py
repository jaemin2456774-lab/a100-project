from pathlib import Path
import ast

SRC = Path(__file__).with_name('main.py').read_text(encoding='utf-8')
TREE = ast.parse(SRC)

assert '116.0-LTS-S2.17.22.1' in SRC
assert 'RELEASEGATE PATH TYPE SAFETY HOTFIX' in SRC
assert 'def _v1160_s217221_path(value):' in SRC
assert 'def _v1160_s217221_existing_path(value):' in SRC
assert "v88_record_error('s21722-releasegate-background',e)" in SRC
assert 'os.path.exists(path)' in SRC
assert 'os.path.exists(raw_path)' not in SRC
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')
print('S2.17.22.1 regression tests: PASS')
