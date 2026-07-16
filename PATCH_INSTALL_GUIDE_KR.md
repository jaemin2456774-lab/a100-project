# S2.17.49 패치 설치 안내

1. Railway 배포 저장소의 프로젝트 루트 `main.py`를 패치 파일로 덮어씁니다.
2. 기존 `/data`, 환경 변수, Railway Volume은 삭제하거나 초기화하지 않습니다.
3. 커밋 후 Railway에서 새 Deployment를 실행합니다.
4. 로그에서 S2.17.49 startup preflight PASS와 Registry 341을 확인합니다.
5. `/version`, `/versionaudit`, `/commandcert`, `/releasegate detail`, `/ltsreadiness detail`, `/runtimehealth`, `/errors` 순서로 검증합니다.
