"""A100 V91.8 offline Scenario Decision Engine regression test."""
from __future__ import annotations
import importlib.util, os, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ.setdefault("TELEGRAM_BOT_TOKEN","")
os.environ.setdefault("TELEGRAM_CHAT_ID","")
os.environ.setdefault("COINGLASS_API_KEY","")
os.environ.setdefault("DATABASE_URL","")
with tempfile.TemporaryDirectory(prefix="a100_v918_scenario_") as tmp:
    os.environ["A100_DATA_DIR"]=tmp
    spec=importlib.util.spec_from_file_location("a100_v918_scenario",ROOT/"main.py")
    module=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(module)
    row={"symbol":"NFPUSDT","side":"LONG","last_price":0.19,"final_score":82.0,"confidence":84.0,
         "change_24h":5.2,"stage":"ENTRY","meta_decision":"TRADE","recommendation_grade":"A",
         "risk_state":{"mode":"NORMAL"},"similarity_stats":{"trades":24,"win_rate":62.5,"expectancy_pct":1.4}}
    out=module._v918_scenario_from_row(row)
    assert out["entry_state"]=="TRIGGERED"
    assert len(out["scenarios"])==5
    assert round(sum(x["probability"] for x in out["scenarios"]),1)==100.0
    assert all(x["invalidation"]>0 for x in out["scenarios"])
    assert out["scenarios"][0]["probability"]>=out["scenarios"][-1]["probability"]
    late=module._v918_scenario_from_row(dict(row,change_24h=18.0))
    assert late["entry_state"]=="LATE"
    halted=module._v918_scenario_from_row(dict(row,risk_state={"mode":"HALT"}))
    assert halted["entry_state"]=="INVALID"
    pre=module.v91_preflight(); assert pre["ok"],pre
    assert pre["command_count"]>=138
    assert callable(module.V90_COMMAND_REGISTRY["scenario"])
    assert callable(module.V90_COMMAND_REGISTRY["scenario_top"])
    assert not pre["help_audit"]["usage_missing"]
    assert module._v91_default_state()["schema"]==1
print("A100 V91.8 scenario decision regression test: PASS")
