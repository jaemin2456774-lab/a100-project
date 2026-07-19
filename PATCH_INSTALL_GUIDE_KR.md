# Railway 설치 안내

1. ZIP의 `main.py`를 기존 프로젝트 `main.py`에 덮어씁니다.
2. 기존 `/data`, 환경변수, 학습 데이터는 삭제하지 않습니다.
3. Railway에서 재배포 후 `/version`, `/versionaudit`, `/help`, `/errors`를 실행합니다.
4. `/help`의 카테고리별 버튼을 하나씩 눌러 PASS/PARTIAL/FAILED/PENDING 상태를 검수합니다.

주의: PARTIAL은 오류가 아니라 Handler 실행은 성공했지만 실제 Runtime Evidence가 아직 PASS 조건에 도달하지 않은 상태입니다.
