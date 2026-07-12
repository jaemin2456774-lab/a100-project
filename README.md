# A100 V101.0 Closed Loop Learning Development

기준 버전: V100.0 Learning Intelligence.

## 핵심 변경
- `/aiunified SYMBOL` 실행 시 추천 신호를 별도 학습 DB에 자동 저장
- 기존 Paper/Shadow 종료 기록과 추천을 자동 매칭해 WIN/LOSS/HOLD 판정
- 거래량·OI·Funding·압축·Momentum·Pattern·Cycle·MTF 가중치 안전 학습
- 저성과 전략은 충분한 표본 이후 자동 `DISABLED`
- 신규 명령: `/learningcore`, `/autotrack`, `/weightboard`, `/strategyboard`

## 안전성
- 기존 `a100_v91_paper_state.json`과 Schema 1 유지
- 학습 상태는 `a100_v101_learning_state.json`에 분리 저장
- Paper 20개, Shadow 60개 한도 유지
- 실거래 주문 경로 추가 없음
