# A100 V116.2 RC2.3.4 릴리스 노트

- Engine E2E Performance counter의 `performance_outcomes` 키 매핑을 복구했습니다.
- Outcome/Attribution/Performance 레코드를 단일 필드가 아닌 ID alias 교집합으로 비교합니다.
- 명시적 Performance 행이 없는 기존 저장소는 durable performance counter를 사용하되 완료 Outcome 수를 상한으로 적용합니다.
- orphan, duplicate, revision-only, performance-unlinked 레코드는 삭제하지 않고 진단에 보존합니다.
- Version Audit에 완료 체인과 raw durable counter를 함께 표시합니다.
- Gate, Threshold, Learning, Shadow/Paper/Live 주문 로직은 변경하지 않았습니다.
