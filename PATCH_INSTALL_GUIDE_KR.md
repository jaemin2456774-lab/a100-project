# 설치 안내

1. 현재 Railway 프로젝트와 `/data` 볼륨을 유지합니다.
2. 패치의 `main.py`만 기존 프로젝트의 `main.py`에 덮어씁니다.
3. `A100_BASELINE.md`, `BASELINE_FEATURES.json`, 테스트와 매니페스트는 저장소 루트에 추가합니다.
4. 환경변수와 설정 파일은 변경하지 않습니다.
5. 재배포 후 `/version`, `/versionaudit`, `/releasegate`, `/status`, `/errors`를 확인합니다.

정상 기준: 341/341, Schema 1, Paper 20, Shadow 60, Live OFF, Startup Preflight PASS, 신규 치명 오류 없음.
