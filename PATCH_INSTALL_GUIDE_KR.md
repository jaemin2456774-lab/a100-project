# S2.17.28.1 긴급 패치 설치 안내

기존 프로젝트의 `main.py`만 덮어쓰고 Railway를 재배포합니다. `/data`, 환경변수, 설정 파일은 변경하거나 삭제하지 마십시오.

정상 로그 기준:

- `A100 V116.0-LTS-S2.17.28.1 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`

`certification preflight findings:`가 표시될 수 있으나 운영 필수 검사에 문제가 없다면 프로세스는 종료되지 않습니다. 설치 후 `/version`, `/versionaudit`, `/runtimehealth`, `/releasegate`, `/errors`를 확인하십시오.
