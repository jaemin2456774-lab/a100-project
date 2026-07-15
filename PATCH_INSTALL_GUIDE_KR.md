# 설치 안내

1. 기존 프로젝트와 `/data` 볼륨을 보존합니다.
2. 패치 ZIP의 `main.py`만 기존 프로젝트에 덮어씁니다.
3. Railway/GitHub에 반영하고 재배포합니다.
4. 시작 로그에서 `S2.17.22`와 startup preflight PASS를 확인합니다.
5. Telegram에서 아래 명령을 순서대로 실행합니다.

```text
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- 버전 `V116.0-LTS-S2.17.22`
- `OUTCOME STATISTICS ENGINE V1 · SCHEMA 1`
- `PRODUCTION READINESS DASHBOARD V7 · VERIFIED DATA`
- Registry/Callable/Routes 341/341
- 신규 runtime error 없음
- `/releasegate`와 `/versionaudit`의 Snapshot ID 및 Unified Hash 일치
