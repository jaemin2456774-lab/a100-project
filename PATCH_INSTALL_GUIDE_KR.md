# S2.17.27 패치 설치 안내

1. Railway의 기존 프로젝트 파일 중 `main.py`만 이 패치의 파일로 덮어씁니다.
2. `/data`, 환경변수, 설정 및 학습 데이터는 삭제하거나 초기화하지 않습니다.
3. 재배포 후 시작 로그에서 S2.17.27, 명령 341개, preflight PASS를 확인합니다.

## 설치 후 실행 순서
`/version` → `/runtimehealth` → `/runtimehealth` → `/releasegate` → `/releasegate` → `/commandperformance` → `/versionaudit` → `/errors`

## 기대 결과
- `/runtimehealth`가 120초 제한에 걸리지 않아야 합니다.
- `/releasegate` 실행 뒤 `s21725-releasegate-background TimeoutError`가 새로 기록되지 않아야 합니다.
- 모든 현재 출력 헤더는 `A100 V116.0-LTS-S2.17.27`이어야 합니다.
- 실제 점수가 기준 미달이면 Gate BLOCKED는 정상입니다.
