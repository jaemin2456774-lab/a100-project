# A100 V91.4 Fast Learning Shadow Trading Engine

V91.3의 Self-Learning·Explainable Signal 기능을 유지하면서, 단기간에 더 많은 학습 표본을 확보하기 위한 Shadow Trading 엔진을 추가한 버전입니다.

## 핵심 변경

- 실전형 Paper 동시 포지션 기본 15개
- LONG/SHORT 기본 한도 각각 9개
- 종목 재진입 쿨다운 기본 30분
- 후보 감시 기본 40개
- 자동 스캔 기본 주기 120초
- Shadow 학습 포지션 기본 30개, 최대 200개
- WATCH·READY·ENTRY 단계별 독립 시나리오 기록
- Shadow 포지션은 실제 Paper 노출·한도를 소모하지 않음
- 같은 종목도 단계별(WATCH/READY/ENTRY)로 별도 성과 추적
- TP·SL·시간청산, MFE·MAE, 시장국면, 전략, 신뢰도 기록
- 실전형 Paper 결과와 Shadow 결과를 분리 저장
- 실계좌 주문 기능은 계속 미구현·비활성

## 신규 명령

- `/papershadow` : Shadow 엔진 상태
- `/papershadowpositions` : 열린 Shadow 시나리오
- `/papershadowperformance` : 국면·방향·신호단계·전략별 성과

## 권장 Railway 환경변수

```text
PAPER_MAX_POSITIONS=15
PAPER_MAX_LONG_POSITIONS=9
PAPER_MAX_SHORT_POSITIONS=9
PAPER_DEFAULT_NOTIONAL=30
PAPER_SYMBOL_COOLDOWN_MINUTES=30
PAPER_CANDIDATE_LIMIT=40
PAPER_SCAN_SECONDS=120

PAPER_SHADOW_ENABLED=1
PAPER_SHADOW_MAX_POSITIONS=30
PAPER_SHADOW_COOLDOWN_MINUTES=10
PAPER_SHADOW_INCLUDE_WATCH=1
PAPER_SHADOW_INCLUDE_READY=1
PAPER_SHADOW_INCLUDE_ENTRY=1
PAPER_SHADOW_TIME_STOP_MINUTES=240
PAPER_SHADOW_SL_PCT=2
PAPER_SHADOW_TP_PCT=4
PAPER_SHADOW_CAPTURE_TOP=40
PAPER_LEARNING_INCLUDE_SHADOW=0
```

처음 24시간은 Shadow 30개로 운영하고, 오류·API 429·처리지연이 없을 때 60개, 이후 100개로 단계 확대하는 것을 권장합니다.

## 주의

Shadow 성과는 실제 Paper 성과와 별도 집계됩니다. 기본값 `PAPER_LEARNING_INCLUDE_SHADOW=0`이므로, Shadow 표본이 기존 AI Score 보정에 바로 섞이지 않습니다.
