# A100 V116.1 DEV S59.7.22

## Shadow Entry Gate Trace & Learning Source Alignment

- READY/WATCH 학습 시나리오와 ENTRY 후보를 명확히 분리
- ENTRY 0의 실제 원인을 점수 격차, 단계 미도달, 중복, 쿨다운, 한도로 표시
- 최근 후보 상위 3개의 Stage, Score, ENTRY Gap 표시
- Candidate Snapshot에 최대 20개의 진단용 요약을 영속 저장
- Shadow 전용 Self Review 및 Accuracy 표본을 durable source 기준으로 재집계
- 기존 `review 0 / accuracy 0` 오표시 수정
- 통합 Learning Queue/Worker/Attribution 수치는 별도로 유지
- 점수 임계값, Stage 분류, Gate Formula, 주문 로직 변경 없음
- Registry 341/341, Runtime First, Strict Read Only, Live OFF 유지
