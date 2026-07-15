# S2.17.16 패치 설치 안내

1. Railway/GitHub의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. `/data` 폴더와 환경변수는 삭제하거나 초기화하지 않습니다.
3. 배포 로그에서 S2.17.16, Registry 341, Preflight PASS를 확인합니다.
4. Telegram에서 `/version`, `/releasegate`, `/versionaudit`, `/errors`를 순서대로 실행합니다.
5. `/releasegate`와 `/versionaudit`의 Snapshot ID/Unified Hash가 동일한지 확인합니다.

유지: Schema 1 / Paper 20 / Shadow 60 / Live Trading OFF.
