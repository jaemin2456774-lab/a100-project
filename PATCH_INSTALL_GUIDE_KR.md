# S58.4 Railway 설치 및 확인

패치를 저장소 루트에 덮어쓰고 Railway로 배포합니다.

먼저 실행:
/status
/runtimehealth
/buildinfo
/routeraudit
/versionaudit
/connectivity
/pipelineaudit
/engineaudit
/strategytrust
/memoryhealth
/releasegate
/dashboard
/errors
/performanceaudit

그 다음 확인:
/commandcert
/commandcert detail
/commandmatrix
/regressionguard
/verifyall
/errors

승인 기준:
- `/engineaudit` S58.4 제목과 Build ID
- 실행한 PARTIAL 명령에 `RUNTIME_CERT`
- Command Cert PASS 증가 / PARTIAL 감소
- FAILED 0 / DISCONNECTED 0
- Registry 341/341
- Errors 0
