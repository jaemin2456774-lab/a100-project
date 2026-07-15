# S2.17.25 패치 설치 안내

1. 기존 프로젝트와 `/data`, 환경변수, 설정 파일을 유지합니다.
2. ZIP의 `main.py`를 기존 프로젝트에 덮어씁니다.
3. 테스트 파일과 문서는 운영에 필수는 아니지만 GitHub 검증용으로 함께 업로드할 수 있습니다.
4. Railway를 재배포합니다.

## 시작 로그
- `A100 V116.0-LTS-S2.17.25 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`

## 설치 후 확인 명령
`/version`, `/status`, `/dashboard` 2회, `/strategytrust`, `/outcomequality`, `/releasegate`, `/versionaudit`, `/commandcert`, `/pipelinetrace`, `/ltscertification`, `/runtimehealth`, `/commandperformance`, `/latency`, `/errors`

## 필수 캡처
Railway 시작 로그, `/version`, `/versionaudit`, `/strategytrust`, `/outcomequality`, `/releasegate` 전체, `/dashboard` 연속 2회, `/runtimehealth`, `/errors`.

점수가 기준 미달이면 BLOCKED가 정상이며 패치가 점수를 임의로 높이지 않습니다.
