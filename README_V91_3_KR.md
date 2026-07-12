# A100 V91.3 Self-Learning Explainable Signal Engine

기준 원본: 정상 작동이 확인된 V91.2 ZIP
배포 환경: Railway 전용
실계좌 주문: 포함하지 않음

## 주요 추가 기능
- 시장 국면·종목·방향·전략별 최근 Paper 청산 결과 학습
- 최소 표본 수 미달 시 점수 보정 금지
- 학습 점수 보정 상한 적용으로 과최적화 방지
- 기존 후보 점수와 학습 후 최종 점수 동시 표시
- 추천 이유와 감점 이유 생성
- 신뢰도와 사용된 학습 표본 수 표시
- WATCH → READY → ENTRY 3단계 진입 신호
- 기존 청산 알림 체계와 결합 가능한 EXIT 단계 예약
- 동일 종목·방향 알림 쿨다운
- 점수가 상위 단계로 승격되면 쿨다운 중에도 업그레이드 알림
- Paper 자동진입은 ENTRY 단계 후보만 허용

## 신규 명령
- `/paperlearning` : 최근 학습 표본과 국면·방향별 성과
- `/papersignals` : 설명 가능한 최신 후보 신호

## 알림 동작
V91.3 단계 알림은 `PAPER_AUTO_SCAN=1` 및 `PAPER_SIGNAL_ALERTS=1`일 때 후보 스캔 주기에 맞춰 동작합니다.
기존 A100 자동 조건 알림은 그대로 유지됩니다.

## 권장 초기 환경변수
```text
PAPER_AUTO_SCAN=1
PAPER_AUTO_ENTRY=0
PAPER_SIGNAL_ALERTS=1
PAPER_SIGNAL_COOLDOWN_SECONDS=1200
PAPER_SIGNAL_WATCH_SCORE=55
PAPER_SIGNAL_READY_SCORE=68
PAPER_SIGNAL_ENTRY_SCORE=78
PAPER_LEARNING_MIN_SAMPLES=10
PAPER_LEARNING_RECENT_WINDOW=100
PAPER_LEARNING_MAX_ADJUST=12
```

자동진입은 충분한 모의 검증 전까지 `PAPER_AUTO_ENTRY=0`을 유지하세요.
