from pathlib import Path
import ast
SRC=Path(__file__).with_name('main.py').read_text(encoding='utf-8')
ast.parse(SRC)
assert '116.0-LTS-S2.17.26' in SRC
assert 'SHARED SNAPSHOT FAST PATH' in SRC
assert 'def _v1160_s21726_fast_snapshot():' in SRC
assert 'async def status1160ltss21726_cmd' in SRC
assert 'async def pipelinetrace1160ltss21726_cmd' in SRC
assert 'async def ltscertification1160ltss21726_cmd' in SRC
status=SRC.split('async def status1160ltss21726_cmd',1)[1].split('async def pipelinetrace1160ltss21726_cmd',1)[0]
assert '_v1160_s2173_cached_snapshot' not in status
assert "'status':status1160ltss21726_cmd" in SRC.replace(' ','')
assert "'pipelinetrace':pipelinetrace1160ltss21726_cmd" in SRC.replace(' ','')
assert "'ltscertification':ltscertification1160ltss21726_cmd" in SRC.replace(' ','')
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')
print('S2.17.26 regression tests: PASS')
