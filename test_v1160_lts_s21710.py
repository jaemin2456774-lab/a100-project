from pathlib import Path
p=Path(__file__).with_name('main.py')
s=p.read_text(encoding='utf-8')
checks={
 'version': '116.0-LTS-S2.17.10' in s,
 'single_exec': s.count('if __name__ == "__main__":') == 1,
 'exec_last': s.rstrip().endswith('main()'),
 'persistent_restore': 'v1160_lts_certification_snapshot.json' in s and '_v1160_s21710_restore_snapshot_once' in s,
 'atomic_persist': 'os.replace(tmp, V1160_S21710_SNAPSHOT_FILE)' in s,
 'nonblocking_releasegate': 'asyncio.create_task(_v1160_s21710_releasegate_job' in s,
 'nonblocking_versionaudit': 'asyncio.create_task(_v1160_s21710_versionaudit_job' in s,
 'policy_preserved': all(x in s for x in ['Schema 1 · Paper 20 · Shadow 60 · Live OFF','Registry {len(V90_COMMAND_REGISTRY)}/341']),
}
for k,v in checks.items(): print(f'{k}: {"PASS" if v else "FAIL"}')
assert all(checks.values())
