# A100 V116.1 DEV S57.8 Railway 설치 가이드

1. 현재 저장소와 Railway Volume을 백업합니다.
2. ZIP 파일을 저장소 루트에 덮어씁니다.
3. 변경 파일만 GitHub에 커밋·푸시합니다.
4. Railway에서 배포합니다.

시작 로그:
- `V116.1-DEV-S57.8 worker running...`
- `BUILD_ID=S57.8-20260719-METADATA-SINGLE-SOURCE-FINAL-01`
- `metadata single source: ACTIVE`
- `UI major redesign: DEFERRED`

배포 후 확인:
/version
/buildinfo
/routeraudit
/versionaudit
/engineaudit
/status
/runtimehealth
/verifyall
/errors

승인 기준:
- `/version` 제목이 S57.8 현재 제목
- `/version` Identity Audit PASS
- 모든 Audit PASS
- Registry 341/341
- Errors 0
