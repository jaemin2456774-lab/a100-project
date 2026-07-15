# S2.17.35 패치 설치 안내

1. 실행 중인 A100 서비스를 중지합니다.
2. 기존 프로젝트와 데이터 디렉터리를 백업합니다.
3. ZIP의 `main.py`를 기존 프로젝트의 `main.py`에 덮어씁니다.
4. 데이터, 환경변수, 설정 파일은 변경하거나 삭제하지 않습니다.
5. 서비스를 다시 시작합니다.

## 시작 로그 확인
- `A100 V116.0-LTS-S2.17.35 ... worker running...`
- `A100 V91 startup commands: 341`
- `startup preflight: PASS`
- `live runtime worker: ACTIVE`

## 설치 후 확인 명령
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

`/dashboard`는 연속 두 번 실행해 첫 응답과 두 번째 응답의 속도를 비교합니다.
