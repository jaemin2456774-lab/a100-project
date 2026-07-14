import importlib.util
from pathlib import Path


def load_main(tmp_path):
    p=Path(__file__).with_name("main.py")
    spec=importlib.util.spec_from_file_location("a100_s21",p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.V1160_S21_STATE_PATH=str(tmp_path/"runtime.json")
    mod.V1160_S21_PREFLIGHT_CACHE=None
    return mod


def test_s21_preflight_and_registry(tmp_path):
    m=load_main(tmp_path); audit=m.v91_preflight(force=True)
    assert audit["ok"], audit.get("failed")
    assert m.V1160_VERSION_MANAGER.number=="116.0-LTS-S2.1"
    assert len(m.V90_COMMAND_REGISTRY)==341
    assert audit["release_freeze"]=="ACTIVE"
    assert audit["regression_risk"]=="NONE"


def test_runtime_state_persists_and_samples(tmp_path):
    m=load_main(tmp_path)
    view=m._v1160_s21_runtime_view(True)
    assert view["sample_count"] >= 1
    assert Path(m.V1160_S21_STATE_PATH).exists()
    assert 0 <= view["progress"] <= 100
    assert view["state"]["schema"] == 1


def test_runtime_trend_classification(tmp_path):
    m=load_main(tmp_path)
    assert m._v1160_s21_trend_label(None, True)=="🟡 WARMING UP"
    assert m._v1160_s21_trend_label(2.0)=="🟢 STABLE"
    assert m._v1160_s21_trend_label(10.0)=="🟡 WATCH"
    assert m._v1160_s21_trend_label(20.0)=="🔴 DRIFT"


def test_active_long_runtime_handlers(tmp_path):
    m=load_main(tmp_path)
    assert m.V90_COMMAND_REGISTRY["runtimehealth"] is m.runtimehealth1160ltss21_cmd
    assert m.V90_COMMAND_REGISTRY["performanceaudit"] is m.performanceaudit1160ltss21_cmd
    assert m.V90_COMMAND_REGISTRY["dashboard"] is m.dashboard1160ltss21_cmd
