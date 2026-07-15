# S2.17.2 패치 설치 안내

1. ZIP을 해제합니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 교체합니다.
3. Railway 재배포를 실행합니다.
4. 로그에서 `Health server listening on port 8080`이 정확히 1회만 출력되는지 확인합니다.
5. `/version`, `/releasegate`, `/versionaudit`, `/pipelinetrace`, `/errors`를 실행합니다.

데이터 디렉터리와 Railway 영구 볼륨은 삭제하거나 초기화하지 마십시오.
