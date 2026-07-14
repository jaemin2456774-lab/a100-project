# A100 V116.0 LTS-FC1.1 Change Ledger

| ID | 변경 목적 | 수정 영역 | 영향 범위 | 검증 | 회귀 결과 | 상태 |
|---|---|---|---|---|---|---|
| FC1.1-001 | 인증 화면 제품 UI 통일 | `main.py` 공통 Badge/Footer | `/version`, `/status`, `/commandcert`, `/performanceaudit`, `/dashboard` | 출력 테스트 | PASS | CERTIFIED |
| FC1.1-002 | Gate 숫자·상태 정렬 | `status1160ltsfc11_cmd` | `/status` | Plain-text/정렬 테스트 | PASS | CERTIFIED |
| FC1.1-003 | Build Breakdown 및 Evidence Summary | `commandcert1160ltsfc11_cmd` | `/commandcert`, `/commandcert deep` | 341/341 및 출력 테스트 | PASS | CERTIFIED |
| FC1.1-004 | Recent/Startup/Lifetime 상태 배지 | `performanceaudit1160ltsfc11_cmd` | `/performanceaudit` | 3-window 테스트 | PASS | CERTIFIED |
| FC1.1-005 | 실측 기반 Release Readiness | `_v1160_fc11_readiness`, Dashboard | `/dashboard` | 파생 계산 검증 | PASS | CERTIFIED |
| FC1.1-006 | Feature Freeze 및 데이터 보존 | Preflight | Schema 1, Paper 20, Shadow 60, Live OFF | 전체 pytest | PASS | CERTIFIED |
