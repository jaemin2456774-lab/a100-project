# S2.17.41 Railway 설치 안내

1. ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
2. GitHub 저장소에 커밋·푸시합니다.
3. Railway에서 새 배포가 완료될 때까지 기다립니다.
4. 로그에서 S2.17.41 worker, preflight PASS, registered commands 341을 확인합니다.
5. Telegram에서 `/version`, `/versionaudit`, `/commandcert`, `/status`, `/runtimehealth`, `/errors`를 실행합니다.

기존 `/data`, DB, 환경 변수와 설정은 변경하지 않습니다.
