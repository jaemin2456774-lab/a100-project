# A100 V92.4 Consensus & Gold Signal Engine

V92.3의 기존 데이터와 schema 1을 유지하면서 엔진 합의도와 엄격한 Gold Signal을 추가한 버전입니다.

## 신규 명령
- `/consensus BTC` : Pattern, Market, Momentum, Risk, Meta, Timing, Scenario 합의도
- `/gold BTC` : Gold Signal 통과 여부와 미충족 조건
- `/gold_top` : Gold 기준 통과 종목 목록

## 개선 명령
- `/dashboard BTC`
- `/final BTC`
- `/coach BTC`
- `/topscore`
- `/help`, `/commands V92`

## 데이터 호환
- 상태 파일: `a100_v91_paper_state.json`
- schema: `1`
- 기존 Paper, Shadow, Audit, Review, Memory, Confidence History 유지
- 실계좌 주문 경로 없음
