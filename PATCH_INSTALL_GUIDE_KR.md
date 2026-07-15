# S2.17.27 설치 안내

1. 기존 S2.17.26 프로젝트에서 패치 파일을 같은 경로에 덮어씁니다.
2. `/data`, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
3. Railway를 재배포합니다.

정상 시작 로그:
- `A100 V116.0-LTS-S2.17.27 REAL-TIME RUNTIME RECOVERY worker running...`
- `A100 V91 startup commands: 341`
- `A100 S2.17.27 live runtime worker: ACTIVE · interval 2.0s`

확인 명령:
`/version`, `/versionaudit`, `/status` 2회, `/runtimehealth` 2회, `/releasegate`, `/commandperformance`, `/errors`
