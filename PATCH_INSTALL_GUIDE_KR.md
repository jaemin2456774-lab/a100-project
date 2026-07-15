# S2.17.19 패치 설치 안내

1. 현재 GitHub 프로젝트의 `main.py`를 백업합니다.
2. 패치의 `main.py`와 테스트 파일을 프로젝트 루트에 덮어씁니다.
3. 기존 `/data` 볼륨과 환경변수는 변경하지 않습니다.
4. Railway 배포 완료 후 `/version`, `/releasegate`, `/versionaudit`, `/errors`를 순서대로 확인합니다.

정상 기준: Registry/Callable/Routes 341/341, Schema 1, Paper 20, Shadow 60, Live OFF, 신규 오류 0건.
