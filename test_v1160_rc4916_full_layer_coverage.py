import main

def test_rc4916_invariants():
    audit=main.v91_preflight()
    assert audit['ok'], audit.get('failed')
    assert main.V91_VERSION == main.V1160_RC4916_VERSION
    assert len(main.V90_COMMAND_REGISTRY)==341
    view=main._v1160_rc4916_cert_view()
    assert view['registry_verified']==341
    assert view['callable']==341
    assert view['runtime_routes']==341
    assert view['help']==341
    assert main.V91_MAX_POSITIONS==20
    assert main.V914_SHADOW_MAX==60
    assert main._v91_default_state().get('schema')==1

def test_consistent_snapshot_shape():
    snap=main._v1160_rc4916_consistent_snapshot()
    assert snap['id'].startswith('LS-')
    assert isinstance(snap['state'],dict)
    assert isinstance(snap['cert'],dict)
    assert isinstance(snap['forecast'],dict)
