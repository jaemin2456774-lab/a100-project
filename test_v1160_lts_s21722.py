from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parent
SRC=(ROOT/'main.py').read_text(encoding='utf-8')


def test_compile():
    ast.parse(SRC)


def test_version_and_features_present():
    for token in (
        '116.0-LTS-S2.17.22',
        'OUTCOME STATISTICS ENGINE V1',
        'PRODUCTION READINESS DASHBOARD V7',
        'Runtime history merge V2',
        'READY/COLLECTING/IN PROGRESS are display states',
    ):
        assert token in SRC


def test_only_one_executable_block_and_last():
    assert SRC.count('if __name__ == "__main__":') == 1
    assert SRC.rstrip().endswith('if __name__ == "__main__":\n    main()')


def test_no_gate_threshold_override():
    block=SRC[SRC.index('# A100 V116.0-LTS-S2.17.22'):]
    assert 'target=0' not in block
    assert 'synthetic' not in block.lower()
    assert 'cur>=target' in block
