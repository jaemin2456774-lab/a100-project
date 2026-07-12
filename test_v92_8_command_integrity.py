import importlib.util
from pathlib import Path


def load_main():
    p=Path(__file__).with_name('main.py')
    spec=importlib.util.spec_from_file_location('a100_v928_main', p)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_shadow_commands_are_live_callbacks():
    m=load_main()
    required={'papershadowstatus','papershadowpositions','papershadowhistory','papershadowstats'}
    assert required.issubset(m.V90_COMMAND_REGISTRY)
    assert all(callable(m.V90_COMMAND_REGISTRY[x]) for x in required)


def test_v928_version_is_final_and_schema_preserved():
    m=load_main()
    assert m.V91_VERSION == m.V928_VERSION
    assert 'V92.8' in m.V91_VERSION
    assert m._v91_default_state()['schema'] == 1
    assert Path(m.V91_STATE_FILE).name == 'a100_v91_paper_state.json'


def test_help_usage_registry_sync():
    m=load_main()
    assert not (set(m.V925_COMMAND_USAGE) - set(m.V90_COMMAND_REGISTRY))
    assert m.v91_preflight()['ok']


def test_final_callbacks_are_v928():
    m=load_main()
    assert m.V90_COMMAND_REGISTRY['intelligence'] is m.intelligence928_cmd
    assert m.V90_COMMAND_REGISTRY['dashboard'] is m.dashboard928_cmd
    assert m.V90_COMMAND_REGISTRY['final'] is m.final928_cmd
    assert m.V90_COMMAND_REGISTRY['help'] is m.help928_cmd
    assert m.V90_COMMAND_REGISTRY['commands'] is m.commands928_cmd
