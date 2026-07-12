"""A100 V92.0 offline AI Score / Explainable Confidence regression test."""
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

with tempfile.TemporaryDirectory(prefix="a100_v920_") as tmp:
    os.environ["A100_DATA_DIR"] = tmp
    spec = importlib.util.spec_from_file_location("a100_v920", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    row = {
        "symbol": "NFPUSDT", "side": "LONG", "last_price": 0.19,
        "final_score": 84.0, "change_24h": 5.2, "quote_volume": 125_000_000,
        "spread_pct": 0.03, "stage": "ENTRY", "meta_decision": "TRADE",
        "meta_adjust": 3.0, "reasons": ["OI 증가", "음수 펀딩 유지"], "penalties": [],
        "risk_state": {"mode": "NORMAL", "max_drawdown_pct": 2.0, "max_loss_streak": 1},
        "market_context": {"score": 72.0},
        "similarity_stats": {"trades": 24, "win_rate": 64.0, "expectancy_pct": 1.8, "avg_similarity": 0.88},
        "stats": {"trades": 16, "win_rate": 62.5, "avg_pnl": 1.2},
    }
    scored = module._v920_score_from_row(row)
    assert scored["symbol"] == "NFPUSDT"
    assert 0 <= scored["score"] <= 100
    assert scored["grade"] in {"S+", "S", "A+", "A", "B", "C"}
    assert 0 <= scored["confidence"] <= 100
    assert set(scored["components"]) == set(module.V920_SCORE_WEIGHTS)
    assert all(0 <= x <= 100 for x in scored["components"].values())
    assert abs(sum(scored["confidence_breakdown"].values()) - 100.0) <= 0.2
    assert scored["positives"]

    overheated = module._v920_score_from_row(dict(row, change_24h=22.0))
    assert overheated["components"]["Momentum"] < scored["components"]["Momentum"]
    assert any("추격" in reason for reason in overheated["risks"])

    halted = module._v920_score_from_row(dict(row, risk_state={"mode": "HALT"}))
    assert halted["components"]["Risk"] < scored["components"]["Risk"]
    assert any("HALT" in reason for reason in halted["risks"])

    assert module._v920_grade(96) == "S+"
    assert module._v920_grade(92) == "S"
    assert module._v920_grade(87) == "A+"
    assert module._v920_grade(82) == "A"
    assert module._v920_grade(75) == "B"
    assert module._v920_grade(60) == "C"

    preflight = module.v91_preflight()
    assert preflight["ok"], json.dumps(preflight, ensure_ascii=False, indent=2)
    assert preflight["command_count"] >= 138
    assert all(callable(module.V90_COMMAND_REGISTRY[x]) for x in ("score", "explain", "topscore"))
    assert not preflight["help_audit"]["usage_missing"]
    assert module._v91_default_state()["schema"] == 1
    assert module.V91_STATE_FILE.endswith("a100_v91_paper_state.json")

print("A100 V92.0 AI Score and Explainable Confidence regression test: PASS")
