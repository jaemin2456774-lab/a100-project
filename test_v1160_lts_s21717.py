from pathlib import Path

SOURCE = Path(__file__).with_name("main.py").read_text(encoding="utf-8")

def test_single_executable_block():
    assert SOURCE.count('if __name__ == "__main__":') == 1

def test_version_and_engines_present():
    for token in (
        "V1160_LTS_S21717_NUMBER",
        "RUNTIME SCORE EXPLAIN ENGINE V6",
        "EVIDENCE ETA PREDICTOR V2",
        "MANDATORY GATE ACTION PLANNER V4",
        "LTS CERTIFICATION PROGRESS V2",
        "FINAL RECOMMENDATION V2",
    ):
        assert token in SOURCE

def test_registry_rebinding_present():
    assert 'V90_COMMAND_REGISTRY.update({"version":version1160ltss21717_cmd' in SOURCE

def test_executable_block_is_last():
    assert SOURCE.rstrip().endswith('main()')
