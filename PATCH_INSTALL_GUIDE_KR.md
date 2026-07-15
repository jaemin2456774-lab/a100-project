# S2.17.14 패치 설치 안내

1. Railway 서비스를 중지하지 않고 GitHub 저장소의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. `/data` 폴더와 환경변수는 삭제하거나 초기화하지 않습니다.
3. GitHub 커밋 후 Railway 배포가 완료될 때까지 기다립니다.
4. 시작 로그에서 `V116.0-LTS-S2.17.14`와 `startup preflight: PASS`를 확인합니다.
5. Telegram에서 `/version`, `/releasegate`, `/versionaudit`, `/errors`를 순서대로 실행합니다.

정상 기준:
- Registry/Callable/Runtime Route 341/341
- `/releasegate`와 `/versionaudit`의 Snapshot ID 및 Unified Hash 일치
- `RUNTIME WINDOW ENGINE V2`에 시간창별 서로 다른 sample/coverage 표시
- `SNAPSHOT BUILD METRICS V2`에 실제 build last/avg/peak 표시
- 신규 120초 timeout 및 Runtime 오류 없음
