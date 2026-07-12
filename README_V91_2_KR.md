# A100 V91.2 Multi-Symbol Regime Learning Engine

Railway 전용 Paper Trading 확장 버전입니다. 실계좌 주문 기능은 포함하지 않습니다.

## 핵심 추가 기능
- 동시 Paper 포지션 기본 10개
- LONG/SHORT 개별 한도
- 총 가상 노출금액 제한
- 종목별 재진입 쿨다운
- Binance 유효 USDT 종목 기반 알트 후보 스캔
- 거래대금·활동성·스프레드·모멘텀 기반 후보 점수
- 급등 추격 감점 및 BTC 급변 시 알트 자동진입 차단
- 9단계 시장 국면 분류
- 진입 시 시장 국면과 전략 저장
- MFE, MAE, 보유시간, 청산 이유 저장
- 국면·방향·전략별 성과 집계
- Railway 재시작 후 다중 포지션 복원

## 신규 명령
- `/paperregime`
- `/papercandidates`
- `/paperperformance`
- `/paperautostatus`

기존 Paper 명령과 기존 114개 명령은 유지되며 전체 등록 명령은 118개입니다.

## 권장 환경변수
```text
PAPER_TRADING_ENABLED=0
PAPER_AUTO_MONITOR=1
PAPER_MAX_POSITIONS=10
PAPER_MAX_LONG_POSITIONS=6
PAPER_MAX_SHORT_POSITIONS=6
PAPER_MAX_TOTAL_NOTIONAL=1000
PAPER_SYMBOL_COOLDOWN_MINUTES=60
PAPER_CANDIDATE_LIMIT=20
PAPER_CANDIDATE_TOP=10
PAPER_MIN_QUOTE_VOLUME=5000000
PAPER_MAX_SPREAD_PCT=0.35
PAPER_AUTO_SCAN=1
PAPER_AUTO_ENTRY=0
PAPER_SCAN_SECONDS=300
PAPER_AUTO_ENTRY_TOP=2
PAPER_BTC_SHOCK_PCT=2.5
```

초기 운영에서는 `PAPER_AUTO_ENTRY=0`을 유지하고 후보 스캔과 수동 Paper 진입부터 검증하십시오.
