# S2.17.22.1 설치 안내

1. 기존 프로젝트의 `main.py`를 이 패치의 `main.py`로 덮어씁니다.
2. `/data` 볼륨과 환경변수는 삭제하거나 초기화하지 않습니다.
3. Railway에서 재배포합니다.
4. 배포 후 `/version`, `/releasegate`, `/versionaudit`, `/errors` 순서로 확인합니다.

정상 기준:
- 버전 `V116.0-LTS-S2.17.22.1`
- `/releasegate` Summary와 Detail 모두 출력
- `/versionaudit` PASS
- `/errors`에 배포 이후 `s21722-releasegate-background`의 dict/stat TypeError가 새로 기록되지 않음
