# Change Ledger — LTS S2.1

| 항목 | 내용 |
|---|---|
| 변경 목적 | Sprint 2 장시간 운영 안정성 계측 시작 |
| 수정 모듈 | `main.py`, 활성 릴리스 테스트, 릴리스 문서 |
| 영향 명령 | `/version`, `/status`, `/runtimehealth`, `/performanceaudit`, `/dashboard`, `/commandcert` |
| 데이터 영향 | 기존 Schema/학습 데이터 변경 없음. 별도 runtime evidence JSON만 생성 |
| 회귀 검증 | 전체 pytest 83/83 PASS, Registry 341 유지 |
| 승인 상태 | DEVELOPMENT CERTIFIED / LONG RUNTIME MEASURING |
