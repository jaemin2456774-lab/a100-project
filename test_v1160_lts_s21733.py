from pathlib import Path
p=Path("main.py").read_text()
assert "116.0-LTS-S2.17.33" in p
assert "LTS FINAL OPERATIONS CONSOLE" in p
assert "LIVE OPERATIONS OVERVIEW" in p
assert "MANDATORY GATE PROGRESS" in p
assert "Current {current:.1f} / Target {target:.1f}" in p
assert "Remaining {'0.0' if passed else f'+{gap:.1f}'}" in p
assert "Telegram path STRICT READ ONLY" in p
assert "No gate, evidence, file, or snapshot calculation occurs on Telegram." in p
assert "status1160ltss21733_cmd" in p
assert "releasegate1160ltss21733_cmd" in p
assert "dashboard1160ltss21733_cmd" in p
assert "ltscertification1160ltss21733_cmd" in p
print("S2.17.33 regression PASS")
