from pathlib import Path
import ast
p=Path(__file__).with_name("main.py")
s=p.read_text(encoding="utf-8")
ast.parse(s)
assert s.count('if __name__ == "__main__":') == 1
assert s.rstrip().endswith('main()')
for token in ["S2.17.11","PERSISTENT SNAPSHOT V2","Previous snapshot rollback","RUNTIME HISTORY","SHA256"]:
    assert token in s, token
print("S2.17.11 static checks PASS")
