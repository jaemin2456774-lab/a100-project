# S2.17.11 패치 설치 안내
1. ZIP을 풉니다.
2. 저장소 루트의 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 영구 볼륨은 삭제하지 않습니다.
4. GitHub에 커밋한 뒤 Railway 재배포를 확인합니다.
5. `/version`, `/releasegate`, `/versionaudit`, `/errors` 순서로 검증합니다.

첫 실행은 기존 JSON Snapshot 또는 새 Snapshot을 사용하고, 새 Snapshot 생성 뒤 `.bin` 파일이 저장됩니다. 다음 재시작부터 `Binary snapshot restored`가 표시되어야 합니다.
