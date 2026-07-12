# A100 V91.6 Adaptive Strategy Selection Engine

정상 작동이 확인된 V91.5를 기준으로 종목·방향·시장 국면별 전략 선택과 저성과 전략 자동 격리 기능을 추가한 Railway 전용 Paper/Shadow 학습 버전입니다.

## 신규 기능
- 종목별 LONG/SHORT 전략 성과 분리
- 시장 국면별 최적 전략 자동 선택
- 전략 후보: 돌파 모멘텀, 추세 눌림목, 박스 평균회귀, 하락 돌파, 반등 숏
- 표본 수에 따라 국면 적합도와 실제 성과를 점진적으로 혼합
- 충분한 표본에서 저승률·음의 기대값 전략 자동 격리
- 격리 전략은 ENTRY 승격을 차단하고 READY 이하로 제한
- 전략 성과 기반 점수 보정 최대 ±6점
- Paper/Shadow 기록은 계속 분리 유지
- 실계좌 주문 기능은 포함하지 않음

## 신규 명령
- `/paperadaptive` 현재 후보별 선택 전략과 보정치
- `/paperstrategies` 종목·방향·국면별 전략 매트릭스
- `/paperquarantine` 자동 격리된 저성과 전략

## 권장 Railway 환경변수
```
PAPER_STRATEGY_MIN_SAMPLES=12
PAPER_STRATEGY_QUARANTINE_MIN_SAMPLES=20
PAPER_STRATEGY_QUARANTINE_WIN_RATE=40
PAPER_STRATEGY_QUARANTINE_EV_PCT=-0.15
PAPER_STRATEGY_MAX_ADJUST=6
PAPER_STRATEGY_AUTO_QUARANTINE=1
```

초기에는 표본이 부족해 국면 적합도 중심으로 선택하며, 청산 데이터가 쌓일수록 실제 전략 성과 비중이 커집니다.
