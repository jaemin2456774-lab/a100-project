# A100 V91.5 EXPECTANCY PATTERN LIFECYCLE LEARNING ENGINE

기준 원본: V91.4 Fast Learning Shadow Trading Engine
배포 환경: Railway 전용
실계좌 주문: 미포함·비활성

## 핵심 추가 기능

- Paper와 Shadow 청산 결과를 통합한 패턴 메모리
- 종목·방향·신호단계·전략·시장국면별 통계
- 베이지안 보정 승률과 기대값(EV) 계산
- 평균 수익·평균 손실·손익비·예상 보유시간 계산
- 최소 표본 미달 시 N등급 처리
- A+~D 추천 등급
- 기대값 기반 점수 보정은 최대 ±5점으로 제한
- Shadow 포지션의 ADD·부분익절·본전이동·트레일링 후보 단계 기록
- 실제 Paper와 Shadow 포지션·성과 데이터는 계속 분리 저장

## 신규 명령

- `/paperexpectancy` : 후보별 기대값·보정승률·등급
- `/paperpatterns` : 시장국면·방향·단계·전략별 패턴 성과
- `/paperlifecycle` : 열린 Shadow의 거래 생애주기 진행 상태

전체 명령 수: 126개

## 권장 환경변수

```text
PAPER_PATTERN_MIN_SAMPLES=8
PAPER_PATTERN_WINDOW=1000
PAPER_PATTERN_PRIOR_TRADES=10
PAPER_PATTERN_PRIOR_WIN_RATE=50
PAPER_LIFECYCLE_PARTIAL_R=0.50
PAPER_LIFECYCLE_BREAKEVEN_R=0.65
PAPER_LIFECYCLE_TRAILING_R=0.80
```

## 배포 후 점검

```text
/selfcheck
/watchdog
/papershadow
/paperexpectancy
/paperpatterns
/paperlifecycle
```
