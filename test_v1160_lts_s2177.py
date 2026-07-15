from pathlib import Path

source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
assert "116.0-LTS-S2.17.7" in source
assert "Cache Hit Rate" in source
assert "Expires In" in source
assert "Last Miss Reason" in source
assert source.count('if __name__ == "__main__":') == 1
print("S2.17.7 static checks: PASS")
