# Railway 배포 및 QA

패치의 main.py를 저장소 main.py에 덮어쓴 뒤 Railway에서 재배포합니다.

실행 순서:
/version
/buildinfo
/runtimehealth
/versionaudit
/papershadowperformance
/papershadowperformance
/papershadow
/coverageplan
/errors

기대값:
- Registry 341/341
- Version Audit PASS
- 두 번째 performance: Bounded QA Cache H1/M1, Snapshot Read 약 0ms, 2000ms 이하
- v55 cache save warning 재발 없음
