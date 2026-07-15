from pathlib import Path

text = Path('main.py').read_text(encoding='utf-8')
assert 'V1160_LTS_S21714_VERSION' in text
assert 'RUNTIME WINDOW ENGINE V2' in text
assert 'SNAPSHOT BUILD METRICS V2' in text
assert 'EMA stabilized' in text
assert text.count('if __name__ == "__main__":') == 1
assert text.rstrip().endswith('main()')
print('S2.17.14 static regression: PASS')
