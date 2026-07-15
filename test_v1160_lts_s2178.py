from pathlib import Path
p=Path(__file__).with_name("main.py").read_text()
assert "116.0-LTS-S2.17.8" in p
assert "Cache Requests" in p and "Snapshot Build" in p
assert "Policy Fingerprint" in p and "TTL expired" in p
assert p.count('if __name__ == "__main__":') == 1
print("S2.17.8 static tests PASS")
