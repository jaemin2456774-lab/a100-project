# S2.12 패치 설치

1. 현재 GitHub 저장소의 `main.py`를 백업합니다.
2. 패치의 `main.py`만 저장소 루트에 덮어씁니다.
3. Commit 후 Railway 재배포를 확인합니다.
4. 배포 후 `/version`, `/status`, `/runtimehealth`, `/dashboard btc`, `/releasegate`, `/versionaudit`, `/pipelinetrace`, `/errors`를 순서대로 실행합니다.

주의: 점수 보정은 정보성 Forecast만 변경합니다. 기존 Mandatory Gate 기준과 데이터는 변경하지 않습니다.
