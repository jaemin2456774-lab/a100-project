# S58.4.2 Railway 설치 및 확인

1. 현재 저장소와 Railway Volume을 백업합니다.
2. ZIP을 저장소 루트에 덮어씁니다.
3. 변경 파일만 커밋하고 Railway로 배포합니다.

시작 로그:
- `V116.1-DEV-S58.4.2 worker running...`
- `BUILD_ID=S58.4.2-20260719-LEDGER-SAFE-READ-ROUNDTRIP-01`
- `ledger roundtrip selftest: PASS`
- `ledger safe read: ACTIVE`

배포 후 먼저 실행:
/status
/runtimehealth
/buildinfo
/connectivity
/engineaudit
/strategytrust
/memoryhealth
/releasegate
/dashboard
/errors

그 다음 확인:
/commandcert
/commandmatrix
/regressionguard
/verifyall
/errors

승인 기준:
- Ledger roundtrip PASS
- Ledger entries 1 이상
- 실행한 PARTIAL 명령에 RUNTIME_CERT
- Command PASS 증가 / PARTIAL 감소
- Identity, Regression Guard, VerifyAll PASS
- FAILED 0 / DISCONNECTED 0
- Errors 0
