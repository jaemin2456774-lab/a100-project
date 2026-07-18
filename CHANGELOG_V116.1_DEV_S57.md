# A100 V116.1 DEV S57 Changelog

## Runtime Identity Recovery · Route Truth Hotfix

- 최종 Telegram dispatcher가 `/buildinfo`, `/connectivity`, `/connectivity detail`, `/verifyall`을 직접 처리하도록 통합.
- S55에서 Registry에 추가된 `/verifyall` 호환 슬롯을 제거하고 최종 dispatcher 호환 라우트로 유지하여 341개 동결 Registry 복구.
- `/verifyall`의 함수 존재 여부 기반 검사를 실제 최종 route resolver 검사로 교체.
- Registry가 341/341이 아니거나 실제 route target이 불일치하면 종합 PASS 금지.
- `/buildinfo`에 expected/actual handler, route source, 실패 검사 항목 표시.
- BUILD_ID 단일 S57 소스 추가.
- Runtime First, Strict Read Only, Synthetic Completion OFF, Gate 계산식, Schema 1, Paper 20, Shadow 60, Live OFF 보존.
