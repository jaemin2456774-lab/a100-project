import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "main.py"
TEXT = SOURCE.read_text(encoding="utf-8")
TREE = ast.parse(TEXT)

EXPECTED = {
    "_v1160_s21724_gate_matrix": "19e520d55b8b262ce3371732b2193a547f0ea233c835737d869abbc4b4d352d7",
    "_v1160_s21726_fast_context": "92e078790fff6dab3913cac52ad226503ac9ae25a33190cbee55456a2cfc7975",
}

def function_hash(name: str) -> str:
    node = next(
        n for n in TREE.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name
    )
    payload = ast.dump(node, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def test_formula_fingerprints_unchanged():
    for name, expected in EXPECTED.items():
        assert function_hash(name) == expected

def test_active_version_and_contract():
    assert 'V1160_LTS_S2182_NUMBER = "116.0-LTS-S2.18.2"' in TEXT
    assert 'V1160_S2182_BASELINE_CONTRACT' in TEXT
    assert 'Formula Fingerprint' in TEXT
    assert 'Score Formula        UNCHANGED FROM S2.18.1' in TEXT

def test_safety_baseline_preserved():
    required = [
        '"telegram_commands": 341', '"schema": 1', '"paper": 20',
        '"shadow": 60', '"live": "OFF"',
        "V90_EXPECTED_COMMANDS=frozenset(V90_COMMAND_REGISTRY)",
        "'version':version1160ltss2182_cmd",
        "'versionaudit':versionaudit1160ltss2182_cmd",
        "'status':status1160ltss2182_cmd",
        "'runtimehealth':runtimehealth1160ltss2182_cmd",
        "'releasegate':releasegate1160ltss2182_cmd",
        "'ltscertification':ltscertification1160ltss2182_cmd",
        "'pipelinetrace':pipelinetrace1160ltss2182_cmd",
    ]
    for item in required:
        assert item in TEXT

def test_single_executable_block_is_last():
    assert TEXT.rstrip().endswith('if __name__ == "__main__":\n    main()')
    assert TEXT.count('if __name__ == "__main__":') == 1
