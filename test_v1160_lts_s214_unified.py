from pathlib import Path

SOURCE = Path(__file__).with_name("main.py").read_text(encoding="utf-8")


def test_version():
    assert 'V1160_LTS_S214_NUMBER = "116.0-LTS-S2.14"' in SOURCE


def test_unified_snapshot():
    assert "def _v1160_s214_certification_snapshot" in SOURCE


def test_handlers():
    for name in (
        "status1160ltss214_cmd",
        "runtimehealth1160ltss214_cmd",
        "dashboard1160ltss214_cmd",
        "releasegate1160ltss214_cmd",
    ):
        assert name in SOURCE


def test_single_final_entrypoint():
    assert SOURCE.count('if __name__ == "__main__":') == 1
    assert SOURCE.rstrip().endswith("main()")
