# A100 V116.0-LTS-S2.17.22

## Outcome Statistics / History Merge / Gate UI Finalization

- Schema 1의 canonical 및 legacy 종료 기록을 함께 읽는 Outcome Statistics Engine V1 추가
- 숫자 손익이 없는 WIN/LOSS 기록은 승률에만 사용하고 기대값·MDD·비용 지표에는 사용하지 않도록 분리
- Net Win Rate, Net Expectancy, Profit Factor, Average Win/Loss, Maximum Drawdown 집계
- Fee/Slippage/Regime/Complete-row coverage 표시
- Runtime history, runtime evidence, persisted snapshot 및 ETA/metrics state를 중복 제거해 합치는 Runtime History Merge V2 추가
- Gate 표시 상태와 실제 PASS 의미를 분리: 목표 도달만 PASSED로 집계
- Production Readiness Dashboard V7에서 실제 데이터 부족 순서대로 병목 정렬
- /releasegate 및 /versionaudit 비차단 응답과 동일 immutable snapshot 사용 유지
- Schema 1, Paper 20, Shadow 60, Live OFF, /data 보존
