import importlib.util
from pathlib import Path
def test_s26():
 p=Path(__file__).with_name("main.py"); s=importlib.util.spec_from_file_location("a100_s26",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
 assert m.V1160_LTS_S26_NUMBER=="116.0-LTS-S2.6"
 assert sum(m.V1160_S26_WEIGHTS.values())==100
 assert len(m.V90_COMMAND_REGISTRY)==341
 assert m.v91_preflight(force=True)["ok"]
