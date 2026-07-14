import main


def test_rc4917_active_version_and_handlers():
    assert main.V91_VERSION == main.V1160_RC4917_VERSION
    assert main.V90_COMMAND_REGISTRY['version'] is main.version1160rc4917_cmd
    assert main.V90_COMMAND_REGISTRY['help'] is main.help1160rc4917_cmd
    assert main.V90_COMMAND_REGISTRY['commands'] is main.commands1160rc4917_cmd
    assert len(main.V90_COMMAND_REGISTRY) == 341


def test_rc4917_output_normalization_and_probe_cycle():
    assert main._v1160_rc4917_plain('<b>LEARNING FORECAST</b>') == 'LEARNING FORECAST'
    before=len(main.V1160_RC4917_PROBE_EVIDENCE)
    checked=main._v1160_rc4917_probe_step(25)
    assert checked == 25
    assert len(main.V1160_RC4917_PROBE_EVIDENCE) >= before
    assert not main.V1160_RC4917_PROBE_ERRORS


def test_rc4917_preflight_and_invariants():
    audit=main.v91_preflight()
    assert audit['ok'], audit.get('failed')
    assert main._v91_default_state().get('schema') == 1
    assert main.V91_MAX_POSITIONS == 20
    assert main.V914_SHADOW_MAX == 60
