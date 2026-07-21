# 설치 및 Runtime QA

1. ZIP을 기존 프로젝트 루트에 덮어씁니다.
2. Railway에 재배포합니다.
3. 아래 순서로 실행합니다.

```text
/version
/buildinfo
/runtimehealth
/versionaudit
/trustgate
/trustgate
/intelligencescore
/commandcert
/errors
```

## 정상 기대값

```text
Registry 341/341
Runtime Identity PASS
Version Audit PASS
Runtime Integrity 100%
```

`/trustgate`를 연속 두 번 실행해도 Ledger chain event 수가 증가하지 않아야 합니다.

V75 백업 관련 로그에 아래 오류가 다시 나타나면 안 됩니다.

```text
No such file or directory: a100_v75_hybrid_backup.json.tmp
```

정상 저장은 고유 임시 파일을 사용하며 최종 파일로 원자적으로 교체됩니다.
