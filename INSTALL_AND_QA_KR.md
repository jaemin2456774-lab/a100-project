# 설치 및 QA

기존 프로젝트의 main.py만 덮어쓴 뒤 Railway 재배포.

검증 순서:
/version
/buildinfo
/runtimehealth
/versionaudit
/papershadow
/papershadow
/papershadowperformance
/errors

기대: Registry 341/341, Version Audit PASS, Engine E2E Same-ID PASS, 두 번째 Dashboard Cache HIT.
