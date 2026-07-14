# GitHub 덮어쓰기 업데이트

1. 기존 런타임 데이터와 환경변수는 유지합니다.
2. 이 ZIP의 프로젝트 파일을 저장소 루트에 덮어씁니다.
3. `__pycache__`, `.pytest_cache`, 임시 로그는 업로드하지 않습니다.
4. 배포 후 `/version`, `/status` 2회, `/performanceaudit`, `/commandcert`를 검증합니다.
