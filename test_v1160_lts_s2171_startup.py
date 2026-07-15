from pathlib import Path

source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
assert source.count('if __name__ == "__main__":') == 1
assert 'if __name__ == "__main__":\n    main()' in source
assert 'def _v1160_s2171_post_start_warmup()' in source
assert 'start_health_server_once()\n    _v1160_s2171_post_start_warmup()' in source
assert 'V116.0-LTS-S2.17.1' in source
print("S2.17.1 startup ordering static regression: PASS")
