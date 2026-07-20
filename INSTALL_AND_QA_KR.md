# Railway 설치 및 QA

기존 프로젝트의 `main.py`만 덮어쓴 뒤 Railway에서 재배포합니다. `/data`, 환경변수와 기존 학습 데이터는 유지합니다.

검증 순서:

```text
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

기대 결과:
- Registry 341/341
- Version Audit PASS
- Completed Same-ID Outcome = Attribution = Performance
- READY HISTORY 1 이상(READY 후보 관측 후)
- 두 번째 Dashboard/Performance Cache HIT
- Errors 0
