# S2.17 패치 설치

1. ZIP에서 `main.py`를 꺼냅니다.
2. GitHub 저장소 루트의 기존 `main.py`를 완전히 교체합니다.
3. GitHub에서 교체된 파일 크기와 커밋 내용을 확인한 뒤 Railway 재배포를 실행합니다.
4. 배포 후 `/version`이 반드시 `V116.0-LTS-S2.17`을 표시하는지 먼저 확인합니다.
5. `/versionaudit`와 `/pipelinetrace` 제목에도 `S2.17`이 표시되어야 합니다.
6. `/status`, `/runtimehealth`, `/dashboard btc`, `/releasegate`의 `Snapshot ID`와 `Unified score hash`가 같아야 합니다.

기존 데이터 폴더와 Railway 볼륨은 삭제하지 않습니다.
