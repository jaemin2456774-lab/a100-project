# S59.7.13 Railway 설치 안내

1. ZIP의 `main.py`를 GitHub 저장소의 기존 `main.py`에 덮어씁니다.
2. Railway 배포 완료 후 재시작 로그에서 S59.7.13 Build ID를 확인합니다.
3. `/version`, `/versionaudit`, `/championstability`, `/help`, `/errors` 순서로 검증합니다.
4. `/help`에서 카테고리 버튼을 누르고 각 명령 버튼을 하나씩 실행하여 캡처합니다.

기대값:
- Registry 341/341
- Version Audit PASS
- Champion Adaptive Samples/EV/MDD가 본문과 일치
- Help 버튼 1회 클릭당 명령 1회 실행
- 신규 오류 없음
