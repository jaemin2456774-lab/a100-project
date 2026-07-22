# A100 V118.0 RC3.7 릴리즈 노트

Build ID: V118.0-RC3.7-20260722-PERFORMANCE-ALIAS-AUTHORITATIVE-ROUTE-COMPATIBILITY-01

## 변경 사항
- `/performancebudget`을 기존 authoritative `/performance` 경로로 위임합니다.
- `/perf`를 기존 authoritative `/performance` 경로로 위임합니다.
- Alias는 Registry에 추가하지 않아 341/341 계약을 유지합니다.
- `/performance` 출력에 Registry-neutral alias 안내를 추가했습니다.
- 기존 BootManager, Architecture Guard, Deferred Matrix Recovery, Warm Cache 정책을 유지합니다.

## 불변 조건
- Runtime First
- Strict Read Only
- Ledger Append Only
- Registry 341/341
- Live Trading OFF
- 기존 데이터와 환경변수 변경 없음
