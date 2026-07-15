# S2.17.40 패치 설치 안내

1. 기존 Railway 서비스의 데이터 볼륨과 환경 변수는 변경하지 않습니다.
2. ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. 변경 파일을 GitHub에 커밋/푸시한 뒤 Railway 배포를 실행합니다.
4. 시작 로그에서 `S2.17.40`과 `startup preflight: PASS`를 확인합니다.
5. 아래 명령을 순서대로 실행합니다.

```
/version
/versionaudit
/commandcert
/status
/dashboard
/releasegate
/ltscertification
/runtimehealth
/pipelinetrace
/errors
```
