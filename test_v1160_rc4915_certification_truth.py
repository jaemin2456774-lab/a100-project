import main

def test_rc4915_active_version_and_handlers():
    assert main.V91_VERSION == main.V1160_RC4917_VERSION
    assert main._v1160_rc4912_version_number() == main.V1160_RC4915_NUMBER
    assert main.V90_COMMAND_REGISTRY['versionaudit'] is main.versionaudit1160rc4915_cmd
    assert main.V90_COMMAND_REGISTRY['commandcert'] is main.commandcert1160rc4915_cmd

def test_rc4915_registry_truth():
    view=main._v1160_rc4915_cert_view(main._v91_default_state())
    assert view['total']==341
    assert view['registry_verified']==341
    assert view['callable']==341
    assert view['help']==341
    assert view['runtime_probed'] + view['pending_runtime'] == 341

def test_rc4915_preflight():
    audit=main.v91_preflight()
    assert audit['ok'], audit.get('failed')
    assert audit['command_count']==341

def test_rc4915_public_partial_status():
    assert main._v1160_rc4914_public_status('PARTIAL_ENGINE') == 'PARTIAL'
