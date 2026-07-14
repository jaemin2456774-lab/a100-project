from pathlib import Path

SOURCE = Path(__file__).with_name('main.py').read_text(encoding='utf-8')

def test_version_and_handlers_present():
    assert '116.0-LTS-S2.15' in SOURCE
    for name in ('status1160ltss215_cmd','runtimehealth1160ltss215_cmd','dashboard1160ltss215_cmd','releasegate1160ltss215_cmd'):
        assert f'def {name}' in SOURCE

def test_single_final_exec_block():
    assert SOURCE.count('if __name__ == "__main__":') == 1
    assert SOURCE.rstrip().endswith('main()')

def test_consistency_features_present():
    for text in ('Snapshot ID','Pipeline live source','72H CERTIFICATION PROGRESS','Current {current:.1f} · Target {required:.1f}'):
        assert text in SOURCE

def test_frozen_limits_preserved():
    assert 'V91_MAX_POSITIONS == 20 and V914_SHADOW_MAX == 60' in SOURCE
    assert 'place_live_order' in SOURCE
