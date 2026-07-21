# A100 V116.2 RC2.4.6 릴리스 노트

- Safe QA Runner 스레드 전용 Historical Mutation Firewall 추가
- QA Probe 중 closed-loop 재동기화 및 durable state 저장 억제
- Probe 전후 anomaly 증가 감지 시 MUTATION_BLOCKED 격리
- Command 결과 immutable key upsert 및 중복 append 방지
- 20초 이상 명령 Slow Queue 분리
- Batch 종료 Historical Reconciliation 추가
- 현재 보존 이력을 RC2.4.6 Isolation Baseline으로 1회 고정하고 이후 증가만 차단
- Gate, Threshold, Learning, Paper, Live 로직 변경 없음
