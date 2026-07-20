# A100 V116.1 DEV S59.7.21

## Shadow Symbol Quarantine & Snapshot Recovery

- Shadow 감사 루프에서 한 개의 잘못된 심볼이 전체 Producer를 중단하던 문제 수정
- `BINANCE:BTCUSDT`, `BTC/USDT`, `BTC-USDT`, `BTCUSDT.P` 등 일반 표기 정규화
- 빈 심볼, 형식 오류, 거래소 유효 목록 제외 심볼을 개별 격리
- 유효한 후보는 계속 WATCH/READY/ENTRY로 처리
- 후보가 0건이어도 `shadow_candidate_audit` Snapshot을 항상 기록
- 잘못된 심볼 예시와 사유별 누적 건수 표시
- 반복 심볼 오류를 개별 V88 로그 대신 요약 집계
- 시스템 Producer 오류와 데이터 격리 이벤트를 분리
- Registry 341/341, Runtime First, Strict Read Only, Live OFF 유지
