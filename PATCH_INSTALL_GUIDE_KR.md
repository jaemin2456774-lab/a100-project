# S2.17.8 패치 설치
1. ZIP을 해제합니다.
2. `main.py`를 GitHub 저장소 루트의 기존 파일에 덮어씁니다.
3. 데이터 및 환경변수는 변경하지 않습니다.
4. Railway 재배포 후 `/version`, `/releasegate`, `/versionaudit`, `/errors`를 실행합니다.
5. 두 인증 명령의 Snapshot ID/Hash가 같고, TTL 내 두 번째 요청이 CACHE HIT인지 확인합니다.
