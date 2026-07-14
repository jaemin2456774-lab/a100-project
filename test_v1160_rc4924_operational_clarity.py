import main

def test_rc4924_preflight_and_freeze():
    r=main.v91_preflight(force=True)
    assert r['ok'], r.get('failed')
    assert len(main.V90_COMMAND_REGISTRY)==341
    assert main.V90_EXPECTED_COMMANDS==frozenset(main.V90_COMMAND_REGISTRY)
    assert main.V91_MAX_POSITIONS==20
    assert main.V914_SHADOW_MAX==60

def test_rc4924_routes():
    assert main.V90_COMMAND_REGISTRY['dashboard'] is main.dashboard1160rc4924_cmd
    assert main.V90_COMMAND_REGISTRY['releasegate'] is main.releasegate1160rc4924_cmd
    assert main.V90_COMMAND_REGISTRY['runtimehealth'] is main.runtimehealth1160rc4924_cmd
    assert main.V90_COMMAND_REGISTRY['performanceaudit'] is main.performanceaudit1160rc4924_cmd

def test_rc4924_version_single_source():
    assert main.V91_VERSION==main.V1160_VERSION_MANAGER.version
    assert main._v1160_rc4912_version_number()==main.V1160_VERSION_MANAGER.number
    assert main.V1160_VERSION_MANAGER.number=='116.0-RC4.9.24'
