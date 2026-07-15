# S2.17.18 패치 설치

1. ZIP 압축을 풉니다.
2. GitHub 저장소의 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 폴더와 환경변수는 삭제하거나 변경하지 않습니다.
4. Railway 배포 완료 후 `/version`, `/releasegate`, `/versionaudit`, `/errors` 순서로 확인합니다.

정상 기준: V116.0-LTS-S2.17.18, Registry/Callable/Route 341/341, 신규 오류 0건, 두 인증 명령의 Snapshot ID/Hash 일치.
