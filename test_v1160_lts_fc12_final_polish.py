import importlib.util
from pathlib import Path


def load_main():
    p=Path(__file__).with_name('main.py')
    spec=importlib.util.spec_from_file_location('a100_fc12',p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def test_fc12_preflight_and_registry():
    m=load_main(); audit=m.v91_preflight(force=True)
    assert audit['ok'], audit.get('failed')
    assert m.V1160_VERSION_MANAGER.number=='116.0-LTS-FC1.2'
    assert len(m.V90_COMMAND_REGISTRY)==341


def test_performance_warmup_is_not_degraded():
    m=load_main()
    assert m._v1160_fc12_perf_status({'count':0,'p95':99999,'worst':99999})=='🟡 WARMING UP'
    assert m._v1160_fc12_perf_status({'count':29,'p95':99999,'worst':99999})=='🟡 WARMING UP'
    assert m._v1160_fc12_perf_status({'count':30,'p95':100,'worst':200})=='🟢 GOOD'


def test_build_breakdown_has_percent_and_longest():
    m=load_main()
    rows,total,longest=m._v1160_fc12_build_rows({'metrics':{'scan_ms':100},'build_ms':400},400)
    assert len(rows)==5 and total==400
    assert longest[0]=='Evidence Build'
    assert 0 < longest[2] <= 100
