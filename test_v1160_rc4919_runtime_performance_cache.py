import time
import main


def test_rc4919_release_and_invariants():
    assert main.V91_VERSION == main.V1160_RC4919_VERSION
    assert main.V1160_RC4919_NUMBER == '116.0-RC4.9.19'
    assert len(main.V90_COMMAND_REGISTRY) == 341
    assert main.V91_MAX_POSITIONS == 20
    assert main.V914_SHADOW_MAX == 60


def test_certification_cache_identity_and_speed():
    first = main._v1160_rc4919_certification(False)
    started = time.perf_counter()
    second = main._v1160_rc4919_certification(False)
    elapsed_ms = (time.perf_counter() - started) * 1000
    assert second is first
    assert len(second['evidence']) == 341
    assert not second['errors']
    assert elapsed_ms < 50


def test_preflight_cache_identity_and_speed():
    first = main.v91_preflight()
    started = time.perf_counter()
    second = main.v91_preflight()
    elapsed_ms = (time.perf_counter() - started) * 1000
    assert first is second
    assert second['ok']
    assert elapsed_ms < 50


def test_active_fast_handlers():
    assert main.V90_COMMAND_REGISTRY['version'] is main.version1160rc4919_cmd
    assert main.V90_COMMAND_REGISTRY['versionaudit'] is main.versionaudit1160rc4919_cmd
    assert main.V90_COMMAND_REGISTRY['commandcert'] is main.commandcert1160rc4919_cmd
