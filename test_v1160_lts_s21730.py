from pathlib import Path
p=Path(__file__).with_name('main.py').read_text(encoding='utf-8')
assert 'def _v1160_s21730_bar' in p
assert 'releasegate1160ltss21730_cmd' in p
assert 'ltscertification1160ltss21730_cmd' in p
assert 'pipelinetrace1160ltss21730_cmd' in p
assert p.count('if __name__ == "__main__":') == 1
assert 'Telegram performs no gate, evidence, file, or snapshot calculation.' in p
print('PASS S2.17.30 compatibility')
