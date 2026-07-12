# A100 V92.2 FINAL DECISION & AI COACH ENGINE

## 핵심 기능
- `/final BTC`: Score, Confidence, Precision Gate, 시나리오, 진입·목표·무효화 가격을 한 화면으로 통합
- `/coach BTC`: 지금 행동, 좋은 진입 구간, 취소선, 확인할 위험 조건 안내
- `/confidence_history BTC`: 종목별 Confidence·Score 변화 기록
- `/score BTC`: 실전용 간결 출력으로 정리
- `/topscore`: 메달·등급·Gate 상태를 포함한 가독성 개선

## 명령어 별칭 복구
- `/paper` → `/paperstatus`
- `/shadow` → `/papershadow`
- `/market` → `/paperregime`
- `/meta` → `/papermeta`
- `/ev` → `/paperexpectancy`
- `/ai` → `/papercandidates`

## 데이터 호환
기존 상태 파일 `a100_v91_paper_state.json`과 schema 1을 유지합니다. 기존 Paper, Shadow, 학습, Meta, Scenario, Score, Audit, Memory 데이터는 유지되며 `confidence_history`만 안전하게 추가됩니다.

## 안전 원칙
실계좌 주문 기능은 포함하지 않습니다. 권장 비중은 Paper 분석용 위험비중이며 실제 주문을 실행하지 않습니다.
