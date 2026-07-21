# V117.0 RC5 Release Notes

- QA_CAUSED/UNKNOWN 명령의 PASS 승격을 차단하고 영속 격리합니다.
- Batch provenance reconciliation 전 상태 전환 이벤트 append를 지연합니다.
- 정상 전환만 CERTIFICATION_PROMOTION 이벤트로 Certification Ledger에 기록합니다.
- Historical anomaly 원장은 삭제하거나 정규화하지 않습니다. RC5 시작 이전 이벤트를 보존 baseline으로 고정하고 이후 신규 증가만 인증합니다.
- 격리 명령은 Projection에서 MANUAL_REVIEW/PARTIAL로 유지합니다.
