"""A100 V91.1 offline regression smoke test.
Run after installing requirements: python test_v91_stability.py
No live orders are sent and no Telegram connection is started.
"""
from __future__ import annotations
import importlib.util
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "")
os.environ.setdefault("TELEGRAM_CHAT_ID", "")
os.environ.setdefault("COINGLASS_API_KEY", "")
os.environ.setdefault("DATABASE_URL", "")
os.environ["PAPER_TRADING_ENABLED"] = "1"

with tempfile.TemporaryDirectory(prefix="a100_v911_") as tmp:
    os.environ["A100_DATA_DIR"] = tmp
    spec = importlib.util.spec_from_file_location("a100_v911", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    assert module.v91_preflight()["ok"], module.v91_preflight()
    assert len(module.V90_COMMAND_REGISTRY) == 114

    module.V78_VALID_SYMBOLS = {"BTCUSDT", "ETHUSDT"}
    prices = {"BTCUSDT": 100.0, "ETHUSDT": 200.0}
    module._v91_price = lambda symbol: prices[module._v91_normalize_symbol(symbol)]

    state = module._v91_default_state()
    state["enabled"] = True
    module._v91_save_state(state)

    position = module._v91_open("BTC", "LONG", 100, 2, 4)
    assert position["symbol"] == "BTCUSDT"
    try:
        module._v91_open("BTC", "LONG", 100, 2, 4)
        raise AssertionError("duplicate position was not blocked")
    except RuntimeError as exc:
        assert "중복" in str(exc)

    prices["BTCUSDT"] = 104.5
    closed = module._v91_monitor_once()
    assert len(closed) == 1 and closed[0]["close_reason"] == "TAKE_PROFIT"

    module._v91_open("ETH", "SHORT", 100, 2, 4)
    prices["ETHUSDT"] = 190.0
    result = module._v91_close("ETH", "MANUAL")
    assert result["realized_pnl"] > 0

    persisted = module._v91_load_state()
    assert not persisted["positions"]
    assert len(persisted["closed"]) == 2

print("A100 V91.1 stability smoke test: PASS")
