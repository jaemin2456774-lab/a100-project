# 설치 및 QA

기존 RC1.6 프로젝트의 main.py만 덮어씁니다. `/data`와 환경변수는 보존합니다.

배포 후 실행:

/version
/buildinfo
/runtimehealth
/versionaudit
/papershadowperformance
/papershadowperformance
/papershadow
/errors

기대값: Registry 341/341, Version Audit PASS, 첫/둘째 성능 호출 2000ms 이하(첫 호출은 prewarm 완료 시 HIT).
