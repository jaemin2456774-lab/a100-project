# S57.4 패치 설치 안내

1. ZIP을 GitHub 저장소 루트에 덮어씁니다.
2. 기존 `/data`, 환경변수, Railway 볼륨은 삭제하지 않습니다.
3. Railway에서 새 배포를 실행합니다.
4. 시작 로그에서 아래 항목을 확인합니다.

```text
V116.1-DEV-S57.4 worker running...
BUILD_ID=S57.4-20260719-VERIFYALL-PAYLOAD-FINAL-01
A100 V116.1 DEV S57.4 verifyall internal payload: CURRENT IDENTITY
A100 V116.1 DEV S57.4 authoritative virtual routes: 7/7
A100 V116.1 DEV S57.4 registry identity: 341/341
```

배포 후 확인 명령:

```text
/version
/buildinfo
/routeraudit
/status
/runtimehealth
/verifyall
/verifyall detail
/connectivity detail
/errors
```
