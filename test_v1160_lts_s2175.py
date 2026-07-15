from pathlib import Path

p=Path(__file__).with_name("main.py")
s=p.read_text(encoding="utf-8")
assert "116.0-LTS-S2.17.5" in s
assert "async def versionaudit1160ltss2175_cmd" in s
assert "_v1160_s2175_peek_snapshot" in s
assert s.count('if __name__ == "__main__":') == 1
print("S2.17.5 static regression: 4/4 PASS")
