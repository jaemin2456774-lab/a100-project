# S2.17.37 Railway 패치 설치 안내

1. Railway에 연결된 실제 GitHub 배포 브랜치의 프로젝트 루트에서 `main.py`를 덮어씁니다.
2. 다른 데이터·설정·환경변수 파일은 삭제하거나 초기화하지 않습니다.
3. 변경 파일을 커밋·푸시하고 Railway Deployment가 완료될 때까지 기다립니다.
4. Railway Deployment Logs에서 `S2.17.37`과 startup preflight PASS를 확인합니다.
5. Telegram에서 `/version`, `/versionaudit`, `/status` 순서로 실행합니다.

성공 기준:
- A100 V116.0-LTS-S2.17.37
- PASS · Version source single
- Registry / Callable / Expected 341/341/341
- Schema 1 · Paper 20 · Shadow 60 · Live OFF

Render는 사용하지 않습니다.
