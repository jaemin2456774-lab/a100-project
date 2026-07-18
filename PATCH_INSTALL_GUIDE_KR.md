# A100 V116.1 DEV S57 증분 패치 설치 가이드

1. Railway에 연결된 GitHub 저장소에서 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. 기존 `/data`, 환경변수, Telegram Token, 학습 데이터, Snapshot 파일은 삭제하거나 초기화하지 않습니다.
3. GitHub commit/push 후 Railway 자동 배포를 확인합니다.
4. Railway 로그에서 아래 항목을 확인합니다.

```text
V116.1-DEV-S57 worker running...
BUILD_ID=S57-20260718-ROUTE-TRUTH-REGISTRY-341-01
A100 V116.1 DEV S57 registry identity: 341/341
A100 V116.1 DEV S57 identity audit: PASS
A100 V116.1 DEV S57 /buildinfo /connectivity /verifyall: FINAL DISPATCH ACTIVE
```

5. Telegram에서 순서대로 실행하고 캡처합니다.

```text
/version
/buildinfo
/connectivity
/connectivity detail
/verifyall
/verifyall detail
/errors
/status
/runtimehealth
```

## 승인 기준
- `/buildinfo`, `/connectivity`, `/connectivity detail`이 지원하지 않는 명령으로 나오지 않아야 함
- Registry 341/341
- Identity PASS
- `/verifyall` 종합 PASS
- Errors 0
