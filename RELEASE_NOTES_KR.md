# A100 V118.0 RC3.1 릴리스 노트

## 긴급 수정
- RC3 BootManager에서 Architecture Guard가 registry 343 중간 상태를 즉시 실패 처리하던 문제 수정
- baseline/routes 설치 후 canonical 341 registry reconcile 단계 추가
- Guard 실패 시 bounded retry 1회 후에도 341이 아니면 기존처럼 엄격 실패
- 제거된 비정규 alias 목록과 reconcile 결과를 boot state에 기록

## 유지
- Registry 341/341
- Runtime First / Strict Read Only
- Immutable Ledger / Live Trading OFF
- RC3 성능 계측 및 projection cache 수정 유지
