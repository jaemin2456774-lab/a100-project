import importlib.util
import os
from pathlib import Path

os.environ.setdefault("TELEGRAM_BOT_TOKEN","123456:TESTTOKEN")
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("a100_v927",ROOT/"main.py")
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def test_version_and_data_compatibility():
    assert module.V91_VERSION.startswith("A100 V92.7")
    assert module._v91_default_state()["schema"] == 1
    assert os.path.basename(module.V91_STATE_FILE) == "a100_v91_paper_state.json"


def test_shadow_commands_registered_and_documented():
    required={"papershadowstatus","papershadowpositions","papershadowhistory","papershadowstats"}
    assert required.issubset(module.V90_COMMAND_REGISTRY)
    assert required.issubset(module.V925_COMMAND_USAGE)
    assert all(callable(module.V90_COMMAND_REGISTRY[x]) for x in required)


def test_preflight_passes():
    pre=module.v91_preflight()
    assert pre["ok"], [k for k,v in pre["checks"].items() if not v]


def test_sampling_and_alert_regression():
    assert module.V91_MAX_POSITIONS == 20
    assert module.V912_MAX_LONG == 12
    assert module.V912_MAX_SHORT == 12
    assert module.V914_SHADOW_MAX == 60
    assert module.V925_LEARNING_ALERT_HOURS == 4
