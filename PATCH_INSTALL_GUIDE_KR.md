# A100 V116.0 LTS-S2.9 패치 설치 가이드

기준 버전: `A100 V116.0 LTS-S2.8.1`

1. 실행 중인 A100 프로세스를 중지합니다.
2. 기존 프로젝트 폴더와 데이터 폴더를 백업합니다.
3. 이 패치의 파일을 기존 프로젝트 루트에 그대로 덮어씁니다.
4. DB, JSON 상태 파일, 환경변수, 사용자 설정 파일은 삭제하지 않습니다.
5. 재시작 후 아래 명령을 순서대로 확인합니다.

```text
/version
/status
/runtimehealth
/dashboard btc
/releasegate
/commandcert
/commandcert deep
/versionaudit
/pipelinetrace
```

예상 버전: `A100 V116.0-LTS-S2.9`
