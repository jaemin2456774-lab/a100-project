# S58.2 Railway 설치 및 확인

패치를 저장소 루트에 덮어쓰고 Railway로 배포합니다.

확인 명령:
/version
/verifyall
/verifyall detail
/engineaudit
/commandcert
/regressionguard
/errors

승인 기준:
- `/verifyall` 상단 `/version PASS`
- Identity PASS
- Engine E2E PASS
- `/engineaudit` 제목과 Build ID가 S58.2
- Registry 341/341
- Errors 0
