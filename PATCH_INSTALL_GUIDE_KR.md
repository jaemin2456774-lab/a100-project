# S2.13 패치 설치 안내

1. 기존 GitHub 저장소의 `main.py`를 백업합니다.
2. 이 패키지의 `main.py`로 저장소 루트의 `main.py`를 교체합니다.
3. GitHub에 커밋한 뒤 Railway 재배포를 실행합니다.
4. 배포 후 `/version`, `/status`, `/runtimehealth`, `/releasegate`, `/versionaudit`, `/pipelinetrace`, `/errors`를 순서대로 확인합니다.

정상 적용 기준:
- `/version`에 `V116.0-LTS-S2.13` 표시
- `/runtimehealth`에 `Raw / calibrated` 표시
- `/releasegate`에 `Mandatory gates remain authoritative` 표시
