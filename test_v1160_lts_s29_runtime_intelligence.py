import asyncio
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("a100_s29", ROOT / "main.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_s29_preflight_and_registry():
    audit = mod.v91_preflight(force=True)
    assert audit["ok"], audit.get("failed")
    assert mod.V1160_VERSION_MANAGER.number == "116.0-LTS-S2.9"
    assert len(mod.V90_COMMAND_REGISTRY) == 341
    assert mod.V90_COMMAND_REGISTRY["runtimehealth"] is mod.runtimehealth1160ltss29_cmd


def test_s29_health_bands_and_timeline():
    assert mod._v1160_s29_health_band(20).endswith("CRITICAL")
    assert mod._v1160_s29_health_band(40).endswith("DEGRADED")
    assert mod._v1160_s29_health_band(55).endswith("WARNING")
    assert mod._v1160_s29_health_band(70).endswith("HEALTHY")
    assert mod._v1160_s29_health_band(90).endswith("EXCELLENT")
    rows = mod._v1160_s29_evidence_timeline({"cert_elapsed":900}, {"snapshots": []})
    assert len(rows) == 8
    assert "%" in rows[0]


def test_s29_runtimehealth_direct_call(monkeypatch):
    sent = []
    async def fake_reply(update, text, *args, **kwargs):
        sent.append(text)
        return text
    async def fake_base(update, context):
        sent.append("BASE")
        return "BASE"
    monkeypatch.setattr(mod, "v90_1_safe_reply", fake_reply)
    monkeypatch.setattr(mod, "runtimehealth1160ltss26_cmd", fake_base)
    result = asyncio.run(mod.runtimehealth1160ltss29_cmd(object(), object()))
    assert result == "BASE"
    joined = "\n".join(sent)
    assert "RUNTIME INTELLIGENCE" in joined
    assert "SCORE CONTRIBUTIONS" in joined
    assert "EVIDENCE TIMELINE" in joined
