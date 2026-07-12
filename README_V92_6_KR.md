# A100 V92.6 Learning Intelligence & Expanded Sampling

기준선은 검증된 V92.5이며 기존 상태 파일 `a100_v91_paper_state.json`과 schema 1을 그대로 유지합니다.

## 핵심 변경
- Paper 기본 최대 포지션 20개
- LONG/SHORT 각각 최대 12개
- Shadow 학습 포지션 60개
- 후보·Shadow 캡처 60개
- Shadow 쿨다운 5분, 시간청산 240분
- Shadow 표본 학습 포함 기본 ON
- 학습 목표 표본 150건
- WATCH 0.25 / READY 0.60 / ENTRY 1.00 단계별 품질 가중치
- AI Decision 카드형 출력과 최대 10개 판단 근거
- Historical Similarity 표본·승률·기대값 표시
- Dashboard/Final에 별점, AI Confidence, Memory, Similarity 표시
- 4시간 자동 리포트에 최근 24시간 승률, 추세, Paper/Shadow OPEN, 진행률 표시

## 기본 환경값
```env
PAPER_MAX_POSITIONS=20
PAPER_MAX_LONG_POSITIONS=12
PAPER_MAX_SHORT_POSITIONS=12
PAPER_CANDIDATE_LIMIT=60
PAPER_SCAN_SECONDS=120
PAPER_SHADOW_MAX_POSITIONS=60
PAPER_SHADOW_CAPTURE_TOP=60
PAPER_SHADOW_COOLDOWN_MINUTES=5
PAPER_SHADOW_TIME_STOP_MINUTES=240
PAPER_LEARNING_INCLUDE_SHADOW=1
A100_LEARNING_TARGET_SAMPLES=150
A100_LEARNING_ALERT_ENABLED=true
A100_LEARNING_ALERT_HOURS=4
```

실주문 경로는 추가하지 않았습니다.
