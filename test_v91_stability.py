"""A100 V91.6 offline adaptive strategy regression smoke test.
No live orders, Telegram polling, Binance network, or real account calls are made.
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
os.environ["PAPER_MAX_POSITIONS"] = "10"
os.environ["PAPER_MAX_LONG_POSITIONS"] = "6"
os.environ["PAPER_MAX_SHORT_POSITIONS"] = "6"
os.environ["PAPER_MAX_TOTAL_NOTIONAL"] = "1000"
os.environ["PAPER_SYMBOL_COOLDOWN_MINUTES"] = "60"

with tempfile.TemporaryDirectory(prefix="a100_v916_") as tmp:
    os.environ["A100_DATA_DIR"] = tmp
    spec = importlib.util.spec_from_file_location("a100_v916", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    preflight = module.v91_preflight()
    assert preflight["ok"], preflight
    assert len(module.V90_COMMAND_REGISTRY) >= 138
    for command in ("paperregime", "papercandidates", "paperperformance", "paperautostatus", "paperlearning", "papersignals", "papershadow", "papershadowpositions", "papershadowperformance", "paperexpectancy", "paperpatterns", "paperlifecycle", "paperadaptive", "paperstrategies", "paperquarantine"):
        assert callable(module.V90_COMMAND_REGISTRY.get(command))

    module.V78_VALID_SYMBOLS = {"BTCUSDT", "ETHUSDT", "SOLUSDT"}
    prices = {"BTCUSDT": 100.0, "ETHUSDT": 200.0, "SOLUSDT": 50.0}
    module._v91_price = lambda symbol: prices[module._v91_normalize_symbol(symbol)]
    module._v912_regime_snapshot = lambda force=False: {
        "at": 1.0, "regime": "MILD_UPTREND", "btc_price": 100.0,
        "btc_ret_24h": 1.0, "btc_ret_72h": 3.0, "ema20": 99.0,
        "ema50": 97.0, "trend_slope_pct": 2.0, "atr_pct": 1.0,
        "btc_shock": False,
    }

    state = module._v91_default_state()
    state["enabled"] = True
    module._v91_save_state(state)

    btc = module._v91_open("BTC", "LONG", 100, 2, 4, strategy="BREAKOUT")
    eth = module._v91_open("ETH", "SHORT", 100, 2, 4, strategy="REVERSAL")
    assert btc["regime_at_entry"]["regime"] == "MILD_UPTREND"
    assert eth["strategy"] == "REVERSAL"

    try:
        module._v91_open("BTC", "LONG", 100, 2, 4)
        raise AssertionError("duplicate position was not blocked")
    except RuntimeError as exc:
        assert "중복" in str(exc)

    prices["BTCUSDT"] = 102.0
    prices["ETHUSDT"] = 195.0
    module._v91_monitor_once()
    marked = module._v91_load_state()["positions"]
    assert marked["BTCUSDT"]["mfe_pnl"] > 0
    assert marked["ETHUSDT"]["mfe_pnl"] > 0

    prices["BTCUSDT"] = 104.5
    closed = module._v91_monitor_once()
    assert any(row["symbol"] == "BTCUSDT" and row["close_reason"] == "TAKE_PROFIT" for row in closed)

    result = module._v91_close("ETH", "MANUAL", 190.0)
    assert result["realized_pnl"] > 0
    assert result["holding_seconds"] >= 0
    assert result["regime_at_entry"]["regime"] == "MILD_UPTREND"

    persisted = module._v91_load_state()
    assert not persisted["positions"]
    assert len(persisted["closed"]) == 2
    assert persisted["performance"]
    assert "BTCUSDT" in persisted["last_closed_by_symbol"]

    try:
        module._v91_open("BTC", "LONG", 100, 2, 4)
        raise AssertionError("cooldown was not enforced")
    except RuntimeError as exc:
        assert "쿨다운" in str(exc)


    # V91.4 Shadow learning: open independent WATCH/READY/ENTRY scenarios without exposure.
    shadow_row = {"symbol":"SOLUSDT","side":"LONG","stage":"WATCH","strategy":"MOMENTUM_LIQUIDITY",
                  "regime":"MILD_UPTREND","score":60.0,"base_score":60.0,"final_score":60.0,
                  "confidence":55.0,"reasons":["test"],"penalties":[]}
    shadow = module._v914_shadow_open(shadow_row)
    assert shadow and shadow["stage"] == "WATCH"
    assert not module._v91_load_state()["positions"]  # shadow does not consume real Paper slots
    assert len(module._v91_load_state()["shadow_positions"]) == 1
    prices["SOLUSDT"] = 52.5
    shadow_closed = module._v914_shadow_monitor_once()
    assert shadow_closed and shadow_closed[0]["close_reason"] == "TAKE_PROFIT"
    assert shadow_closed[0].get("lifecycle",{}).get("partial") is True
    assert shadow_closed[0].get("lifecycle",{}).get("trailing") is True
    shadow_state = module._v91_load_state()
    assert len(shadow_state["shadow_closed"]) == 1
    assert shadow_state["shadow_performance"]

    # Self-learning: create enough synthetic closed samples and verify bounded adjustment/stage/explanations.
    learned = module._v91_load_state()
    sample = dict(learned["closed"][-1])
    sample.update({"symbol":"SOLUSDT", "side":"LONG", "strategy":"MOMENTUM_LIQUIDITY",
                   "regime_at_entry":{"regime":"MILD_UPTREND"}, "realized_pnl":2.0,
                   "mfe_pnl":3.0, "mae_pnl":-0.5})
    learned["closed"].extend([dict(sample, closed_at=1000+i) for i in range(module.V913_MIN_SAMPLES)])
    module._v91_save_state(learned)
    explained = module._v913_explain_candidate({"symbol":"SOLUSDT","side":"LONG","strategy":"MOMENTUM_LIQUIDITY",
        "regime":"MILD_UPTREND","score":75.0,"quote_volume":100000000,"spread_pct":0.02,"change_24h":5.0})
    assert explained["stats"]["trades"] >= module.V913_MIN_SAMPLES
    assert 0 <= explained["final_score"] <= 100
    assert abs(explained["learning_adjust"]) <= module.V913_MAX_ADJUST
    assert explained["stage"] in {"WATCH","READY","ENTRY"}
    assert explained["reasons"]
    assert explained["recommendation_grade"] in {"N","A+","A","B+","B","C","D"}
    assert "pattern_stats" in explained
    assert explained["pattern_stats"]["smoothed_win_rate"] >= 0
    assert callable(module.V90_COMMAND_REGISTRY.get("paperexpectancy"))

    # V91.6 adaptive strategy selection and quarantine.
    adaptive_state = module._v91_load_state()
    base_closed = dict(adaptive_state["closed"][-1])
    bad=[]
    for i in range(module.V916_QUARANTINE_MIN_SAMPLES):
        row=dict(base_closed)
        row.update({"symbol":"SOLUSDT","side":"LONG","stage":"ENTRY",
                    "strategy":"BREAKOUT_MOMENTUM","regime_at_entry":{"regime":"MILD_UPTREND"},
                    "realized_pnl":-2.0,"notional":100.0,"closed_at":3000+i})
        bad.append(row)
    good=[]
    for i in range(module.V916_QUARANTINE_MIN_SAMPLES):
        row=dict(base_closed)
        row.update({"symbol":"SOLUSDT","side":"LONG","stage":"ENTRY",
                    "strategy":"TREND_PULLBACK","regime_at_entry":{"regime":"MILD_UPTREND"},
                    "realized_pnl":3.0,"notional":100.0,"closed_at":4000+i})
        good.append(row)
    adaptive_state["closed"].extend(bad+good)
    module._v91_save_state(adaptive_state)
    selected, ranking = module._v916_select_strategy("SOLUSDT","LONG","MILD_UPTREND","ENTRY")
    assert selected["strategy"] == "TREND_PULLBACK", (selected, ranking)
    quarantined = [x for x in ranking if x["strategy"] == "BREAKOUT_MOMENTUM"][0]
    assert quarantined["quarantined"] is True
    adaptive = module._v913_explain_candidate({"symbol":"SOLUSDT","side":"LONG","strategy":"MOMENTUM_LIQUIDITY",
        "regime":"MILD_UPTREND","score":75.0,"quote_volume":100000000,"spread_pct":0.02,"change_24h":5.0})
    assert adaptive["strategy"] == "TREND_PULLBACK"
    assert abs(adaptive["strategy_adjust"]) <= module.V916_STRATEGY_MAX_ADJUST
    assert callable(module.V90_COMMAND_REGISTRY.get("paperadaptive"))

print("A100 V91.6 adaptive strategy selection smoke test: PASS")
