# A100 V92.5 AI Decision Intelligence Engine

기준 버전: V92.4 Consensus & Gold Signal Engine 최신 검증 ZIP

## 핵심 추가 기능
- `/intelligence BTC`: AI 최종 판결(BUY/SELL/WATCH/IGNORE/AVOID), Intelligence 점수, Confidence, Consensus, 진입 타이밍, 위험도, Gold 여부, AI 판단 근거 및 주의 조건을 한 화면에 표시합니다.
- `/decisionai BTC`: `/intelligence` 별칭입니다.
- `/learningstatus`: 학습된 트레이딩 승률, 보정 승률, 평가 표본, Precision PASS 성과와 학습 완성도를 즉시 표시합니다.
- `/learningreport`: `/learningstatus` 별칭입니다.
- 4시간마다 Telegram으로 학습 승률·완성도 리포트를 자동 전송합니다.

## 자동 알림 환경변수
- `A100_LEARNING_ALERT_ENABLED=true` 기본값 ON
- `A100_LEARNING_ALERT_HOURS=4` 기본값 4시간
- `A100_LEARNING_TARGET_SAMPLES=100` 완성도 100% 기준 평가 표본
- 기존 `TELEGRAM_CHAT_ID`로 전송됩니다.

## 데이터 및 안전성
- 기존 상태 파일 `a100_v91_paper_state.json` 유지
- schema 1 유지
- 기존 데이터 삭제 및 초기화 없음
- 실주문 기능 추가 없음
- 순수 계산 모듈 `v925_decision_intelligence.py`를 독립 추가하여 기존 엔진과 분리
- 기존 시장 스캔 캐시와 AI Score 결과를 재사용하므로 별도 대규모 API 호출 없음

## 주의
표본이 적을 때 단순 승률은 실제 성능을 과장할 수 있어 V92.5는 베이지안 방식의 보정 승률과 학습 완성도를 함께 표시합니다.
