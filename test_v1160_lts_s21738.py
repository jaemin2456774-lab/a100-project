from pathlib import Path
import ast
p=Path('main.py')
s=p.read_text()
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
for token in [
    'V1160_LTS_S21738_NUMBER = "116.0-LTS-S2.17.38"',
    'async def commandcert1160ltss21738_cmd',
    'async def versionaudit1160ltss21738_cmd',
    "'commandcert':commandcert1160ltss21738_cmd",
    "V90_EXPECTED_COMMANDS=frozenset(V90_COMMAND_REGISTRY)",
    '341 structural command routes certified',
]:
    assert token in s, token
print('S2.17.38 static regression PASS')
