from pathlib import Path
p=Path('main.py').read_text()
required=(
    '116.0-LTS-S2.17.35',
    'LTS FINAL CANDIDATE UI CONSISTENCY',
    '📊 LIVE OPERATIONS',
    '🟢 READY',
    '🟡 MEASURING',
    '🔴 BLOCKED',
    '①', '②', '③', '④', '⑤',
    '🏁 LTS SUMMARY',
    '🚀 PRODUCTION READY · DISPLAY ONLY',
    'Telegram performs no file scan, evidence rebuild, snapshot refresh or gate recomputation.',
    'Registry 341 preserved',
    'status1160ltss21735_cmd',
    'releasegate1160ltss21735_cmd',
    'dashboard1160ltss21735_cmd',
    'ltscertification1160ltss21735_cmd',
)
for token in required:
    assert token in p, token
assert p.rstrip().endswith('if __name__ == "__main__":\n    main()')
assert "'version':version1160ltss21735_cmd" in p
assert "'dashboard':dashboard1160ltss21735_cmd" in p
assert 'width=10' in p
print('S2.17.35 regression PASS')
