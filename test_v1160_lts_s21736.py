from pathlib import Path
import ast
p=Path('main.py').read_text()
ast.parse(p)
required=(
'116.0-LTS-S2.17.36','FINAL UI SYSTEM & PRODUCTION READINESS AUDIT',
'🚦 CERTIFICATION GATES','🏁 LTS FINAL SUMMARY','DISPLAY ONLY · not an authoritative gate',
'Schema 1 · Paper 20 · Shadow 60 · Live OFF','Registry 341 preserved',
'status1160ltss21736_cmd','releasegate1160ltss21736_cmd','dashboard1160ltss21736_cmd','ltscertification1160ltss21736_cmd',
'Telegram performs no file scan, evidence rebuild, snapshot refresh or gate recomputation.'
)
for t in required: assert t in p,t
assert p.rstrip().endswith('if __name__ == "__main__":\n    main()')
assert p.count('if __name__ == "__main__":')==1
assert "'version':version1160ltss21736_cmd" in p
assert "'dashboard':dashboard1160ltss21736_cmd" in p
assert 'width=10' in p
print('S2.17.36 regression PASS')
