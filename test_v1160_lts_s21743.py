import ast, pathlib
p=pathlib.Path('main.py')
s=p.read_text(); ast.parse(s)
assert '116.0-LTS-S2.17.43' in s
assert 'Summary planner active' in s
assert 'Runtime performance view active' in s
assert "len(V90_COMMAND_REGISTRY)==341" in s
assert s.rstrip().endswith('main()')
assert s.count('if __name__ == "__main__":') == 1
print('S2.17.43 static regression PASS')
