# S2.17.26 패치 설치 안내

1. 기존 프로젝트와 `/data`를 유지합니다.
2. ZIP 안의 `main.py`만 기존 프로젝트의 동일 파일에 덮어씁니다.
3. 데이터 파일, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway를 재배포합니다.

## 기대 시작 로그

- `A100 V116.0-LTS-S2.17.26 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`

## 설치 후 확인 명령

`/version`, `/status` 2회, `/pipelinetrace` 2회, `/ltscertification` 2회, `/commandperformance`, `/releasegate`, `/versionaudit`, `/runtimehealth`, `/errors`

첫 호출에서 Shared snapshot이 WARMING이면 오류가 아닙니다. 백그라운드 갱신 후 다시 실행합니다.
