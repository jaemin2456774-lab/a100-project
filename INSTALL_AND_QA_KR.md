# A100 V118.0 RC3.2 설치 및 QA

1. ZIP의 `main.py`를 저장소 루트에 덮어씁니다.
2. Railway에 배포합니다.
3. 배포 시각 이후 로그에서 RC3.2 authoritative 배너와 Registry 341을 확인합니다.
4. 아래 텔레그램 명령을 실행합니다.

```text
/version
/buildinfo
/versionaudit
/performance
/errors
```

## PASS 기준

- `/version`과 `/buildinfo`: V118.0 RC3.2
- Registry: 341/341
- Architecture Guard: PASS
- Version Audit: PASS
- 배포 후 새 `Traceback`, `RuntimeError`, `registry:343` 없음
- 새 Railway 로그에 `V117.0-RC6 worker running` 또는 과거 Build ID 배너 없음

PostgreSQL의 `checkpoint starting/complete` 메시지는 정상 주기 로그입니다.
