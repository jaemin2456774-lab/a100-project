from pathlib import Path
s = Path('main.py').read_text(encoding='utf-8')
assert '116.0-LTS-S2.17' in s
assert 'versionaudit1160ltss217_cmd' in s
assert 'pipelinetrace1160ltss217_cmd' in s
assert 'Unified score hash' in s
assert s.count('if __name__ == "__main__":') + s.count("if __name__ == '__main__':") == 1
assert s.rstrip().endswith('main()')
print('S2.17 static regression: 6/6 PASS')
