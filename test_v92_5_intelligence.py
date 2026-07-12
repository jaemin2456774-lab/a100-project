from __future__ import annotations
import importlib.util, os, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ.setdefault("TELEGRAM_BOT_TOKEN","")
os.environ.setdefault("TELEGRAM_CHAT_ID","")
os.environ.setdefault("COINGLASS_API_KEY","")
os.environ.setdefault("DATABASE_URL","")
with tempfile.TemporaryDirectory(prefix="a100_v925_") as tmp:
    os.environ["A100_DATA_DIR"]=tmp
    spec=importlib.util.spec_from_file_location("a100_v925",ROOT/"main.py")
    module=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(module)
    assert module.V91_VERSION.startswith("A100 V92.6")
    assert module._v91_default_state()["schema"]==1
    assert module.V91_STATE_FILE.endswith("a100_v91_paper_state.json")
    for command in ("intelligence","decisionai","learningstatus","learningreport"):
        assert callable(module.V90_COMMAND_REGISTRY[command])
    q=module._v925_learning_quality({"all":{"n":20,"w":11,"l":7,"f":2,"wr":61.1,"avg":1.2},
                                     "precision":{"n":10,"w":7,"l":3,"f":0,"wr":70.0,"avg":1.8},
                                     "rejected":{"n":10,"w":4,"l":4,"f":2,"wr":50.0,"avg":0.6},
                                     "open":3,"loss_reasons":[]})
    assert 0 <= q["completion"] <= 100
    assert 0 <= q["adjusted_win_rate"] <= 100
    item={"symbol":"BTCUSDT","side":"LONG","score":94,"grade":"S","confidence":88,"stage":"ENTRY",
          "meta_decision":"TRADE","risk_mode":"NORMAL","components":{"Pattern":80,"Liquidity":80,"Momentum":75,
          "Market":75,"Risk":85,"Timing":90,"Learning":70,"Meta":80},"positives":["패턴 강도 양호"],"risks":[]}
    sc={"entry_state":"TRIGGERED","scenarios":[{"probability":60,"entry_low":1,"entry_high":2,"target1":3,"target2":4,"invalidation":0.5}]}
    d=module._v925_decision(item,sc)
    assert d["verdict"] in {"BUY","SELL","WATCH","IGNORE","AVOID"}
    assert d["timing"] in {"NOW","WAIT","CONFIRM"}
    assert d["risk"] in {"LOW","MEDIUM","HIGH"}
    pre=module.v91_preflight(); assert pre["ok"],pre
    assert pre["learning_alert"]["hours"]==4.0
print("A100 V92.5 intelligence regression test: PASS")
