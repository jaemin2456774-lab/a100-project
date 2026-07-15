from pathlib import Path

source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
assert '116.0-LTS-S2.17.3' in source
assert 'releasegate1160ltss2173_cmd' in source
assert 'asyncio.create_task(_v1160_s2173_releasegate_job' in source
assert 'V1160_S2173_RELEASEGATE_TTL = 300.0' in source
assert source.count('if __name__ == "__main__":') == 1
assert source.rstrip().endswith('main()')
print('S2.17.3 static regression tests: PASS')
