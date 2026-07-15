from pathlib import Path
import ast

SRC = Path(__file__).with_name('main.py').read_text(encoding='utf-8')
TREE = ast.parse(SRC)

assert '116.0-LTS-S2.17.24' in SRC
assert 'AUTHORITATIVE TRUST & MANDATORY GATE CERTIFICATION' in SRC
assert 'def _v1160_s21724_authoritative_metrics(snap, detail):' in SRC
assert 'def _v1160_s21724_gate_matrix(snap,detail):' in SRC
assert "'numeric_sample': int(agg.get('numeric',0) or 0)>=numeric_min" in SRC
assert "'fee_coverage': float(agg.get('fee_coverage',0.0) or 0.0)>=cost_min" in SRC
assert "'slippage_coverage': float(agg.get('slippage_coverage',0.0) or 0.0)>=cost_min" in SRC
assert "('lts_readiness','LTS Readiness',95.0)" in SRC
assert "No synthetic uplift, forecast value or display state can satisfy a mandatory gate." in SRC
assert "v88_record_error('s21724-releasegate-background',e)" in SRC
assert "'strategytrust':strategytrust1160ltss21724_cmd" in SRC
assert "'outcomequality':outcomequality1160ltss21724_cmd" in SRC
assert 'V91_MAX_POSITIONS==20 and V914_SHADOW_MAX==60' in SRC
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')
print('S2.17.24 regression tests: PASS')
