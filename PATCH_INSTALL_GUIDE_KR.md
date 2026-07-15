# S2.17.36 패치 설치 안내

1. 현재 운영 폴더와 데이터 폴더를 백업합니다.
2. ZIP의 `main.py`를 기존 프로젝트의 동일 파일 위에 덮어씁니다.
3. 데이터, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. 재시작 후 아래 명령을 순서대로 확인합니다.

/version
/status
/dashboard
/dashboard
/releasegate
/ltscertification
/runtimehealth
/versionaudit
/pipelinetrace
/errors

`/dashboard`는 연속 두 번 실행해 최초 응답과 캐시 응답을 비교합니다.
