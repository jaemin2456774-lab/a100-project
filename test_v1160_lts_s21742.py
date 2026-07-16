from pathlib import Path
import ast

p=Path(__file__).with_name('main.py')
t=p.read_text(encoding='utf-8')
ast.parse(t)
checks={
 'single_exec':t.count('if __name__ == "__main__"')==1 and t.rstrip().endswith('main()'),
 'version': 'V1160_LTS_S21742_NUMBER = "116.0-LTS-S2.17.42"' in t,
 'planner':'coach1160ltss21742_cmd' in t,
 'analyzers':all(x in t for x in ['intelligence1160ltss21742_cmd','strategytrust1160ltss21742_cmd','outcomequality1160ltss21742_cmd','memoryhealth1160ltss21742_cmd','ltsreadiness1160ltss21742_cmd']),
 'registry_guard':"Registry remains 341" in t,
 'read_only':'Strict read-only analyzer source' in t,
 'gate_unchanged':'Gate formulas unchanged' in t,
 'live_off':'Schema 1 · Paper 20 · Shadow 60 · Live OFF' in t,
}
failed=[k for k,v in checks.items() if not v]
print(checks)
if failed: raise SystemExit('FAILED: '+','.join(failed))
print('PASS S2.17.42 static regression')
