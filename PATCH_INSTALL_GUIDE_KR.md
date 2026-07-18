# S46 패치 설치 안내

1. Railway에 연결된 GitHub 저장소에서 ZIP의 `main.py`를 기존 파일에 덮어씁니다.
2. 기존 `/data`, 환경변수 및 설정은 삭제하지 않습니다.
3. Railway 배포 완료 후 startup 로그에서 S46 worker와 Evidence Runtime audit를 확인합니다.
4. 아래 명령을 순서대로 실행합니다.

/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/releasegate detail
/errors

5. 10~15초 안에 `/ultimate`, `/ultimate detail`, `/god`를 다시 실행하여 캐시와 방향 일관성을 확인합니다.
