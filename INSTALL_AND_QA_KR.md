# 설치 및 QA

기존 프로젝트의 `main.py`를 이 패치의 파일로 덮어쓴 뒤 Railway에서 재배포합니다.
기존 `/data`와 환경변수는 유지합니다.

검증 순서:

```
/version
/buildinfo
/runtimehealth
/versionaudit
/papershadow
/papershadowperformance
/errors
```

기대 결과:
- Registry 341/341
- Version Audit PASS
- Engine E2E Same-ID PASS
- Completed Same-ID의 Outcome = Attribution = Performance
- Historical anomalies preserved
- Synthetic completion NONE
- Errors 0
