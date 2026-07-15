from pathlib import Path
s=Path('main.py').read_text(encoding='utf-8')
assert '116.0-LTS-S2.17.13' in s
assert 'CACHE EFFICIENCY V2' in s
assert 'RUNTIME SCORE TREND V2' in s
assert s.count('if __name__ == "__main__":') == 1
print('S2.17.13 static regression PASS')
