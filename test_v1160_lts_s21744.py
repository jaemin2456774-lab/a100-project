import ast, pathlib
p=pathlib.Path('main.py')
s=p.read_text(); ast.parse(s)
assert '116.0-LTS-S2.17.44' in s
assert 'Runtime performance monitor active' in s
assert 'runtime performance monitor: ACTIVE' in s
assert 'Cycle avg / P95 / max' in s
assert "len(V90_COMMAND_REGISTRY)==341" in s
assert 'Gate formulas unchanged' in s
assert s.rstrip().endswith('main()')
assert s.count('if __name__ == "__main__":') == 1
print('S2.17.44 static regression PASS')
