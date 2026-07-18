# A100 V116.1 DEV S57.2 설치 안내

1. Railway에 연결된 GitHub 저장소에서 ZIP의 `main.py`를 기존 파일에 덮어씁니다.
2. 문서 및 manifest 파일은 배포 기록용으로 저장합니다.
3. Railway 새 배포가 시작되면 아래 로그를 확인합니다.

```text
V116.1-DEV-S57.2 worker running...
BUILD_ID=S57.2-20260719-VERSION-RENDERER-SINGLE-SOURCE-01
A100 V116.1 DEV S57.2 application callback: v90_1_dispatch
A100 V116.1 DEV S57.2 route identity: 7/7
A100 V116.1 DEV S57.2 registry identity: 341/341
```

## 배포 후 확인 명령

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

## 승인 기준
- 모든 명령에서 S57.2 Build ID가 일치
- Router Audit PASS
- Build/Application Identity PASS
- Registry 341/341
- VerifyAll 종합 PASS
- Errors 0
