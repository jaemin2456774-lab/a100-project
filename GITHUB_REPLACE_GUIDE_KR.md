# GitHub 덮어쓰기 업데이트

1. 기존 운영 데이터와 `.env`는 유지합니다.
2. 이 ZIP의 프로젝트 파일을 저장소 루트에 그대로 덮어씁니다.
3. `__pycache__`, `.pytest_cache`, 임시 로그는 패키지에 포함하지 않았습니다.
4. `python -m py_compile main.py` 실행 후 배포합니다.
5. 배포 후 `POST_INSTALL_SCREENSHOT_CHECKLIST_KR.md` 순서로 검수합니다.

보존 대상: 상태/학습 데이터, Schema 1, 환경변수. 삭제 금지.
