import copy
import main


def test_rc492_preflight_passes():
    audit=main.v91_preflight()
    assert audit["ok"], [k for k,v in audit["checks"].items() if not v]


def test_execution_cert_is_read_only_and_has_no_failed_handlers():
    state=main._v91_default_state()
    before=copy.deepcopy(state)
    cert=main._v1160_rc492_command_certification(state)
    assert state == before
    assert cert["mode"] == "EXECUTION_BASED_READ_ONLY"
    assert cert["counts"]["FAILED"] == 0


def test_critical_commands_have_executed_engine_evidence():
    cert=main._v1160_rc492_command_certification(main._v91_default_state())
    rows={r["command"]:r for r in cert["rows"]}
    for command in ("releasegate","ltscert","repositoryaudit","healthscore","pipelineaudit","strategytrust","champion","trustgate","runtimehealth","versionaudit"):
        assert rows[command]["executed"], command
        assert rows[command]["engine"], command
        assert rows[command]["status"] == "PASS", (command, rows[command])


def test_policy_and_registry_preserved():
    assert main.V91_MAX_POSITIONS == 20
    assert main.V914_SHADOW_MAX == 60
    assert main._v91_default_state()["schema"] == 1
    assert main.V90_EXPECTED_COMMANDS == frozenset(main.V90_COMMAND_REGISTRY)
    assert main.V90_COMMAND_REGISTRY["commandcert"] is main.commandcert1160rc492_cmd
    assert main.V90_COMMAND_REGISTRY["ltscert"] is main.ltscert1160rc492_cmd
