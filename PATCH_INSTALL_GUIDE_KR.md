# S2.17.3 패치 설치 안내

1. 기존 Railway/GitHub 프로젝트를 백업합니다.
2. 패치의 `main.py`만 저장소 루트의 기존 `main.py`에 덮어씁니다.
3. 데이터 폴더와 Railway Volume은 삭제하거나 초기화하지 않습니다.
4. GitHub에 커밋한 뒤 Railway 재배포를 확인합니다.
5. `/version`, `/releasegate`, `/versionaudit`, `/errors` 순서로 검증합니다.

정상 동작 시 `/releasegate`는 즉시 접수 메시지를 보내고 최종 결과를 별도 메시지로 전송합니다. 기존의 120초 Dispatcher Timeout 오류가 새로 기록되면 안 됩니다.
