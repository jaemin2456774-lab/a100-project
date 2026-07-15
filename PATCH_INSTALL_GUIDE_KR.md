# S2.17.29 설치 안내

1. 기존 프로젝트의 `main.py`를 패치 파일로 덮어씁니다.
2. `/data`, 환경변수와 설정 파일은 삭제하거나 초기화하지 않습니다.
3. Railway를 재배포합니다.

## 정상 시작 로그
- `A100 V116.0-LTS-S2.17.29 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`
- `A100 S2.17.29 live runtime worker: ACTIVE`
- `A100 S2.17.29 evidence change detector: ACTIVE`

## 설치 후 확인
`/version`, `/versionaudit`, `/status` 2회, `/runtimehealth` 2회, `/releasegate` 2회, `/commandperformance`, `/errors`

모든 활성 출력 헤더가 S2.17.29여야 하며, Telegram 명령에서 Gate/Evidence/Snapshot 계산이 발생하면 안 됩니다.
