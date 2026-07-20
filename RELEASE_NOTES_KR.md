# A100 V116.2 RC2.1 Entry Gate Explainability Certification

## 변경 내용
- `/papershadow`, `/papershadowstatus`, `/shadow`에 Entry Decision Explainability 추가
- 후보별 Gate Score / 기준 / Gap / Decision / Top Blocking Reason 표시
- READY 활성 시나리오 체류시간과 후보 관측 READY→ENTRY 단계 변화 추적
- ENTRY/BLOCKED Evidence Ledger를 최대 80건으로 bounded 저장
- 기존 Shadow Learning / Attribution / Queue / Quarantine 검수 유지

## 중요 원칙
- WATCH / READY / ENTRY는 독립 Shadow 학습 시나리오입니다.
- READY→ENTRY 기록은 동일 심볼·방향이 후속 스냅샷에서 다른 단계로 관측된 이력이며 자동 포지션 승격을 의미하지 않습니다.
- Entry Gate 계산식, Threshold, TP/SL, 주문 경로, Live 설정은 변경하지 않았습니다.
