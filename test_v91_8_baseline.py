from __future__ import annotations
import importlib.util
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "")
os.environ.setdefault("TELEGRAM_CHAT_ID", "")
os.environ.setdefault("COINGLASS_API_KEY", "")
os.environ.setdefault("DATABASE_URL", "")

with tempfile.TemporaryDirectory(prefix="a100_v918_") as tmp:
    os.environ["A100_DATA_DIR"] = tmp
    spec = importlib.util.spec_from_file_location("a100_v918", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    assert module.V91_VERSION == "A100 V91.8 SCENARIO DECISION ENGINE"
    assert len(module.V90_COMMAND_REGISTRY) == 135
    assert module.V91_STATE_FILE.endswith("a100_v91_paper_state.json")
    assert module._v91_default_state()["schema"] == 1

    legacy = module._v91_default_state()
    legacy["enabled"] = True
    legacy["closed"] = [{"symbol": "BTCUSDT", "realized_pnl": 1.23}]
    legacy["shadow_closed"] = [{"symbol": "ETHUSDT", "realized_pnl": 2.34}]
    legacy["events"] = [{"seq": 1, "kind": "LEGACY_TEST"}]
    module._v91_save_state(legacy)
    restored = module._v91_load_state()
    assert restored["closed"][0]["symbol"] == "BTCUSDT"
    assert restored["shadow_closed"][0]["symbol"] == "ETHUSDT"
    assert restored["events"][0]["kind"] == "LEGACY_TEST"

    preflight = module.v91_preflight()
    assert preflight["ok"], json.dumps(preflight, ensure_ascii=False, indent=2)
    assert preflight["data_compatibility"]["preserved"] is True

print("A100 V91.8 development baseline compatibility test: PASS")
