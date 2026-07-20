# 설치 및 QA

기존 프로젝트의 `main.py`만 이 패치의 `main.py`로 덮어쓴 후 Railway에서 재배포합니다. `/data`와 환경변수는 유지합니다.

검증 순서:
```
/version
/buildinfo
/runtimehealth
/versionaudit
/papershadow
/papershadow
/papershadowperformance
/papershadowperformance
/errors
```

기대값:
- Registry 341/341
- Version Audit PASS
- `READY TIMELINE V2`, `EVIDENCE LEDGER V2`, `RC2 FINAL QA DASHBOARD` 출력
- 두 번째 `/papershadow` Dashboard Cache HIT
- 두 번째 `/papershadowperformance` Bounded QA Cache HIT
- Gate/Threshold/Live mutation NONE
