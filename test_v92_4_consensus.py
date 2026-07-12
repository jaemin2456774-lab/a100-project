import main


def strong_item():
    return {
        "symbol":"BTCUSDT","side":"LONG","score":96.0,"grade":"S+","confidence":92.0,
        "stage":"ENTRY","meta_decision":"TRADE","risk_mode":"NORMAL",
        "components":{"Pattern":88,"Liquidity":82,"Momentum":78,"Market":80,"Risk":90,"Timing":92,"Learning":76,"Meta":86},
    }


def strong_scenario():
    return {"entry_state":"TRIGGERED","scenarios":[{"probability":48.0,"name":"즉시 돌파","trigger":1,"target1":2,"target2":3,"invalidation":0.5}]}


def test_consensus_strong():
    c=main._v924_consensus(strong_item(),strong_scenario())
    assert c["score"] >= 80
    assert c["status"] == "STRONG"
    assert not c["negative"]


def test_consensus_conflict_blocks():
    x=strong_item(); x["components"]["Market"]=20; x["meta_decision"]="SKIP"; x["risk_mode"]="HALT"; x["components"]["Risk"]=10
    g=main._v924_gate(x,strong_scenario())
    assert not g["passed"]
    assert g["consensus"]["negative"]


def test_gold_strict():
    g=main._v924_gold(strong_item(),strong_scenario())
    assert g["passed"]
    x=strong_item(); x["confidence"]=70
    assert not main._v924_gold(x,strong_scenario())["passed"]


def test_registry_help_and_data_compatibility():
    for name in ("consensus","gold","gold_top","dashboard","final","coach","topscore"):
        assert callable(main.V90_COMMAND_REGISTRY.get(name))
    audit=main._v924_help_audit()
    assert not audit["usage_missing"]
    assert not audit["category_missing"]
    assert len(main.V90_COMMAND_REGISTRY)==153
    assert main.V924_STATE_SCHEMA==1
    assert main.V924_STATE_FILENAME=="a100_v91_paper_state.json"


def test_preflight():
    report=main.v91_preflight()
    assert report["ok"], report
