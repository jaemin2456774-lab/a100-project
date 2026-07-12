# V91.2 변경사항

- V91.1 Paper Stability Engine을 기준으로 확장
- 기본 최대 동시 포지션 3개에서 10개로 변경
- LONG/SHORT별 포지션 한도 추가
- 총 Paper 노출금액 한도 추가
- 종목별 재진입 쿨다운 추가
- 9단계 Market Regime Engine 추가
- Binance 24시간 ticker와 bookTicker 기반 알트 후보 스캔 추가
- 거래대금, 활동성, 모멘텀, 스프레드, 추격 위험을 후보 점수에 반영
- BTC 급변 시 알트 자동진입 차단
- 진입 시 regime 및 strategy 저장
- MFE/MAE, 최고·최저가격, 보유시간 기록
- regime|side|strategy 기준 성과 집계
- Auto Scan 스레드 추가, Auto Entry는 기본 비활성
- 신규 Telegram 명령 4개 추가
- 기존 제외 명령 /arkm, /syn, /sent, /futures 유지
