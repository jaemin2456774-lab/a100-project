# A100 V91.0 AUDITED PAPER TRADING ENGINE

Railway 전용 모의매매 1차 통합본입니다. 실계좌 주문은 구현하지 않았습니다.

## 새 명령
`/paperstatus`, `/paperon`, `/paperoff`, `/paperopen BTC LONG 100 2 4`, `/paperclose BTC`, `/paperpositions`, `/paperhistory`, `/paperkill`, `/paperresetkill`, `/watchdog`

## 기본 안전 설정
- `PAPER_TRADING_ENABLED=0`
- `PAPER_AUTO_MONITOR=0`
- 실계좌 주문 없음
- 심볼 검증 후에만 가격 호출
- 상태는 Railway Volume에 원자적으로 저장
- 일일 손실한도 및 중복 포지션 차단

## Railway 권장 환경변수
```
PAPER_TRADING_ENABLED=0
PAPER_AUTO_MONITOR=1
PAPER_DEFAULT_NOTIONAL=100
PAPER_DEFAULT_SL_PCT=2
PAPER_DEFAULT_TP_PCT=4
PAPER_MAX_POSITIONS=3
PAPER_DAILY_LOSS_LIMIT=100
PAPER_FEE_RATE=0.0004
PAPER_SLIPPAGE_RATE=0.0005
PAPER_MONITOR_SECONDS=15
WATCHDOG_HEARTBEAT_SECONDS=30
```

배포 직후 `/selfcheck`, `/legacycheck`, `/watchdog`, `/paperstatus` 순서로 확인하세요.
