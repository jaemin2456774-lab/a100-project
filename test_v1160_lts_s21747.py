from pathlib import Path
import ast

SRC = Path(__file__).with_name('main.py').read_text(encoding='utf-8')
ast.parse(SRC)

assert 'V1160_LTS_S21747_NUMBER = "116.0-LTS-S2.17.47"' in SRC
assert 'async def versionaudit1160ltss21747_cmd' in SRC
assert "'versionaudit':versionaudit1160ltss21747_cmd" in SRC
assert "V925_COMMAND_USAGE.pop('evidence', None)" in SRC
assert 'Evidence maturity is integrated into /ltsreadiness detail.' in SRC
assert "'Advertised Command Contract', not contract['unsupported']" in SRC
assert "'Startup Migration', migration_ok" in SRC
assert 'Unsupported advertised commands {len(contract["unsupported"])}' in SRC
assert SRC.count('if __name__ == "__main__":') == 1
assert SRC.rstrip().endswith('main()')
print('S2.17.47 static regression PASS')
