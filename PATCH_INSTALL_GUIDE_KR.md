# S2.17.28 패치 설치 안내

1. Railway 프로젝트를 중지하거나 재배포 준비 상태로 둡니다.
2. ZIP의 `main.py`를 기존 프로젝트의 `main.py`에 덮어씁니다.
3. `/data`, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway를 재배포합니다.

## 기대 시작 로그
- `A100 V116.0-LTS-S2.17.28 ... worker running...`
- `A100 V91 startup commands: 341`
- `A100 V91 startup preflight: PASS`

## 설치 후 확인 순서
`/version` → `/versionaudit` → `/runtimehealth` → `/releasegate` → `/status` → `/commandperformance` → `/errors`

## 합격 기준
- 모든 최신 출력 헤더가 S2.17.28
- Version source single PASS
- Registry/Callable/Help/Route 341/341
- `/runtimehealth` 장시간 대기 및 Timeout 없음
- `/releasegate` 실행 후 background TimeoutError 없음
