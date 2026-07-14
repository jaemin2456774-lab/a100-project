import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("a100_rc4922", ROOT / "main.py")
A100 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(A100)


def test_rc4922_release_invariants():
    assert A100.V1160_RC4922_NUMBER == "116.0-RC4.9.22"
    assert A100.V91_VERSION == A100.V1160_RC4922_VERSION
    assert len(A100.V90_COMMAND_REGISTRY) == 341
    assert A100.V90_EXPECTED_COMMANDS == frozenset(A100.V90_COMMAND_REGISTRY)
    assert A100.V91_MAX_POSITIONS == 20
    assert A100.V914_SHADOW_MAX == 60
    assert A100._v91_default_state().get("schema") == 1


def test_output_linkage_and_routes_are_complete():
    cert = A100._v1160_rc4920_build_certification(True)
    view = cert["view"]
    assert view["registry_verified"] == 341
    assert view["callable"] == 341
    assert view["help"] == 341
    assert view["output_linked"] == 341
    assert len(cert["evidence"]) == 341
    assert cert["errors"] == {}


def test_dashboard_delegation_is_detected():
    linked, delegated = A100._v1160_rc4922_has_output(A100.dashboard1160rc4914_cmd)
    assert linked is True
    assert delegated is True


def test_lts_validator_and_preflight():
    assert A100.V90_COMMAND_REGISTRY["ltscertification"] is A100.ltscertification1160rc4922_cmd
    audit = A100.v91_preflight()
    assert audit["ok"] is True
    assert audit["failed"] == []
