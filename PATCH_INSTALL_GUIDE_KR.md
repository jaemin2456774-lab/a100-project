# S2.17.20 패치 설치 안내

1. 기존 GitHub 프로젝트의 `main.py`를 이 패치의 `main.py`로 교체합니다.
2. `/data` 디렉터리와 기존 학습·인증 데이터는 삭제하지 않습니다.
3. 변경 파일만 커밋한 뒤 Railway 재배포를 실행합니다.
4. 배포 후 `/version`, `/releasegate`, `/versionaudit`, `/errors` 순서로 확인합니다.

정상 기준:
- 버전 `V116.0-LTS-S2.17.20`
- Registry/Callable/Runtime Routes 341/341
- Snapshot ID와 Unified Hash가 `/releasegate`, `/versionaudit`에서 동일
- 신규 오류 0건
- 누락된 Strategy Trust 근거는 `N/A`로 표시되며 임의 추정되지 않음
