from pathlib import Path
import ast
S=Path("main.py").read_text()
ast.parse(S)
assert S.count('if __name__ == "__main__":')==1
for token in ["V1160_LTS_S21729_VERSION","_v1160_s21729_refresh_evidence","_v1160_s21729_reply","CHANGE-DRIVEN","STRICT READ ONLY"]: assert token in S
assert "'version':version1160ltss21729_cmd" in S
assert "'status':status1160ltss21729_cmd" in S
assert "'runtimehealth':runtimehealth1160ltss21729_cmd" in S
assert "'releasegate':releasegate1160ltss21729_cmd" in S
print("S2.17.29 regression PASS")
