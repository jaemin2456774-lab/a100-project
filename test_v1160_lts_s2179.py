from pathlib import Path

p = Path(__file__).with_name("main.py")
s = p.read_text(encoding="utf-8")
checks = {
    "version": "V1160_LTS_S2179_NUMBER = \"116.0-LTS-S2.17.9\"" in s,
    "operational_metrics": "Operational Hit Rate" in s and "Cold Start Misses" in s,
    "proactive_refresh": "_v1160_s2179_proactive_refresh_loop" in s,
    "runtime_guard": "v1160_s2179_runtime_certification.jsonl" in s,
    "single_exec": s.count('if __name__ == "__main__":') == 1,
    "exec_last": s.rstrip().endswith('main()'),
}
failed = [k for k, v in checks.items() if not v]
print(checks)
if failed:
    raise SystemExit("FAILED: " + ", ".join(failed))
print("PASS", len(checks), "/", len(checks))
