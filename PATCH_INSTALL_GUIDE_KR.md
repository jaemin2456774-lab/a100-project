# S57.1 Railway 설치 가이드

1. 현재 저장소를 백업합니다.
2. 패치 ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. 기존 `/data`, 환경변수, 설정 파일은 수정하지 않습니다.
4. GitHub 반영 후 Railway에서 재배포합니다.
5. Railway 로그에서 아래 문구를 확인합니다.

```text
V116.1-DEV-S57.1 worker running...
BUILD_ID=S57.1-20260718-APP-CALLBACK-VIRTUAL-ROUTE-01
A100 V116.1 DEV S57.1 application callback: v90_1_dispatch
A100 V116.1 DEV S57.1 virtual route audit: 4/4
A100 V116.1 DEV S57.1 registry identity: 341/341
```

## Telegram 확인 순서

```text
/version
/buildinfo
/routeraudit
/connectivity
/connectivity detail
/verifyall
/verifyall detail
/status
/runtimehealth
/errors
```
