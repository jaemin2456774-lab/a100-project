import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("v927",ROOT/"v927_learning_calibration.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_sample_guard_limits_shift():
    x=mod.calibrated_confidence(70,0,10,0,20)
    assert x["sample_guard"] is True
    assert abs(x["calibrated"]-70)<=2.0


def test_mature_learning_can_adjust_but_is_bounded():
    x=mod.calibrated_confidence(60,150,80,100,20)
    assert x["sample_guard"] is False
    assert 60 < x["calibrated"] <= 68


def test_main_registers_shadow_aliases():
    text=(ROOT/"main.py").read_text()
    for name in ("papershadowstatus","papershadowhistory","papershadowstats"):
        assert f'"{name}"' in text
    assert 'V927_VERSION' in text
    assert 'schema":1' in text or 'schema")==1' in text
