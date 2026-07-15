# S2.17.29.1 설치 안내

1. 현재 S2.17.29 배포를 중지합니다.
2. 패치의 `main.py`를 프로젝트 루트의 기존 파일에 덮어씁니다.
3. `/data`, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway에 재배포합니다.

정상 시작 로그:
- `A100 V116.0-LTS-S2.17.29.1 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`
- `A100 S2.17.29.1 live runtime worker: ACTIVE · interval 2.0s`
- `A100 S2.17.29.1 evidence change detector: ACTIVE · check interval 30.0s`

확인 명령:
`/version`, `/versionaudit`, `/status`, `/runtimehealth`, `/releasegate`, `/commandperformance`, `/errors`
