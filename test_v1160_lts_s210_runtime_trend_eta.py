import asyncio
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('a100_s210', ROOT / 'main.py')
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_s210_preflight_registry_and_version():
    audit = mod.v91_preflight(force=True)
    assert audit['ok'], audit.get('failed')
    assert mod.V1160_VERSION_MANAGER.number == '116.0-LTS-S2.10'
    assert len(mod.V90_COMMAND_REGISTRY) == 341
    assert mod.V90_COMMAND_REGISTRY['runtimehealth'] is mod.runtimehealth1160ltss210_cmd
    assert mod.V90_COMMAND_REGISTRY['releasegate'] is mod.releasegate1160ltss210_cmd


def test_s210_velocity_profile_and_eta_safety():
    rows = [
        {'ts': 1000.0, 'learning': 10, 'target': 20},
        {'ts': 4600.0, 'learning': 12, 'target': 20},
    ]
    values, source, selected, eta_h, remaining = mod._v1160_s210_velocity_profile({'samples': rows}, rows[-1])
    assert values['Overall'] > 0
    assert source in {'1h', '6h', '24h', 'Overall'}
    assert selected > 0
    assert remaining == 8
    assert eta_h and eta_h > 0
    assert mod._v1160_s210_eta_text(None) == 'COLLECTING DATA'
    assert mod._v1160_s210_eta_text(-2) == 'COLLECTING DATA'


def test_s210_memory_stats():
    rv = {
        'state': {'samples': [
            {'memory_mb': 100.0}, {'memory_mb': 120.0}, {'memory_mb': 110.0}
        ]},
        'latest': {'memory_mb': 110.0},
    }
    baseline, current, peak, delta = mod._v1160_s210_memory_stats(rv)
    assert baseline == 100.0
    assert current == 110.0
    assert peak == 120.0
    assert round(delta, 1) == 10.0


def test_s210_runtimehealth_direct_call(monkeypatch, tmp_path):
    sent = []
    async def fake_reply(update, text, *args, **kwargs):
        sent.append(text)
        return text
    async def fake_base(update, context):
        sent.append('BASE')
        return 'BASE'
    monkeypatch.setattr(mod, 'v90_1_safe_reply', fake_reply)
    monkeypatch.setattr(mod, 'runtimehealth1160ltss29_cmd', fake_base)
    monkeypatch.setattr(mod, 'V1160_S210_SCORE_FILE', str(tmp_path / 'score.json'))
    result = asyncio.run(mod.runtimehealth1160ltss210_cmd(object(), object()))
    assert result == 'BASE'
    joined = '\n'.join(sent)
    assert 'RUNTIME ANALYTICS S2.10' in joined
    assert 'MEMORY DETAIL' in joined
    assert 'RUNTIME SCORE DELTA' in joined
