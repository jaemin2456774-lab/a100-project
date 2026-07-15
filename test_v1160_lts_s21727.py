from pathlib import Path
import ast

p=Path(__file__).with_name("main.py")
s=p.read_text(encoding="utf-8")
ast.parse(s)
assert "REAL-TIME RUNTIME RECOVERY" in s
assert "a100-s21727-live-runtime" in s
assert "V1160_S21727_LIVE_INTERVAL = 2.0" in s
assert "Worker → Live Runtime State → Telegram Read Only" in s
assert "Snapshot      Certification / Recovery Fallback" in s
assert s.count('if __name__ == "__main__":') == 1
assert "'status': status1160ltss21727_cmd" in s
assert "'runtimehealth': runtimehealth1160ltss21727_cmd" in s
assert "'releasegate': releasegate1160ltss21727_cmd" in s
print("S2.17.27 real-time runtime recovery static regression: PASS")
