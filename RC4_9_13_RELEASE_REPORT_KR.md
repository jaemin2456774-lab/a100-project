# RC4.9.13 릴리스 보고서

## 수정 원인
RC4.9.12 시작 시 RC4.9.10 및 RC4.9.11의 VersionManager/Handler 동일성 검사가 누적되어 정상 최신 버전도 부팅되지 않았습니다.

## 수정 사항
- Startup Integrity를 현재 활성 릴리스 기준 검사로 변경
- `v1160_rc4910_*`, `v1160_rc4911_*`, `v1160_rc4912_*` 등 과거 RC 전용 요구 조건을 런타임 게이트에서 제거
- 현재 Registry, 현재 Handler, Schema 1, Paper 20, Shadow 60, Live OFF만 Release Blocking 검사
- 과거 검사 결과는 진단 이력으로만 유지하며 부팅 의존성에서 제외
- 기존 데이터와 설정 경로 보존

## 핵심 회귀 방지
앞으로 버전 상승 시 이전 RC 검사 키가 누적되어도 활성 Startup Gate에는 포함되지 않습니다.
