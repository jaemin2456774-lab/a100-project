# S59.7.5 Railway 증분 패치 설치

1. ZIP을 풀고 `main.py`를 저장소 루트의 기존 `main.py`에 덮어씁니다.
2. 기존 `/data` Runtime/Learning 파일과 Railway 환경변수는 변경하지 않습니다.
3. GitHub에 커밋/푸시한 뒤 Railway 배포 완료를 확인합니다.
4. 시작 로그에서 Build ID `S59.7.5-20260719-CURRENT-ROUTE-WORKER-REPLAY-RC-SYNC-01`, Registry 341/341, Live OFF를 확인합니다.

## 배포 후 검증 명령
/version
/versionaudit
/runtimehealth
/status
/crossengineaudit
/evidencereplay
/rcpreflight
/commandmatrix
/ledgeraudit
/releasegate
/errors

주의: `/crossengine`, `/rcpredictor`, `/coverage`, `/ledger`는 Registry 정식 명령이 아닙니다. 위 대응 명령을 사용합니다.
