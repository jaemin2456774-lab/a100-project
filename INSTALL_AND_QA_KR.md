# Railway 설치 및 QA

1. ZIP의 `main.py`를 기존 프로젝트에 덮어씁니다.
2. Railway에서 재배포합니다.
3. 아래 명령을 순서대로 실행합니다.

```text
/version
/buildinfo
/runtimehealth
/versionaudit
/versionaudit
/papershadow
/papershadowperformance
/errors
```

## 확인 기준
- Registry 341/341
- Current Engine E2E Same-ID PASS
- 첫 Version Audit에서 baseline CREATED 또는 ACTIVE
- 두 번째 Version Audit에서 baseline ACTIVE
- Post-baseline Delta orphan/duplicate/attribution 모두 0
- Version Audit PASS
- Errors 0
