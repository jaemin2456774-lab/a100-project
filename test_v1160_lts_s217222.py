from pathlib import Path
import ast
import json

ROOT = Path(__file__).parent
SRC = (ROOT / 'main.py').read_text(encoding='utf-8')
TREE = ast.parse(SRC)
BASELINE = json.loads((ROOT / 'BASELINE_FEATURES.json').read_text(encoding='utf-8'))

assert '116.0-LTS-S2.17.22.2' in SRC
assert 'GOLDEN BASELINE LOCK & PATH TYPE SAFETY' in SRC
assert 'def _v1160_s217221_path(value):' in SRC
assert 'def _v1160_s217221_existing_path(value):' in SRC
assert "v88_record_error('s21722-releasegate-background',e)" in SRC
assert 'os.path.exists(path)' in SRC
assert 'os.path.exists(raw_path)' not in SRC
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')

# Golden baseline invariants: no later experimental certification layers.
for forbidden in BASELINE['forbidden_runtime_markers']:
    assert forbidden not in SRC, forbidden
for required in BASELINE['required_runtime_markers']:
    assert required in SRC, required

print('S2.17.22.2 golden baseline regression tests: PASS')
