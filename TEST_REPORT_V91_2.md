# A100 V91.2 Test Report

## 통과 항목
- Python bytecode compile: PASS
- AST parse: PASS
- 전체 모듈 import: PASS
- V91 preflight: PASS
- 등록 명령 수: 118
- 신규 콜백 4개 연결: PASS
- LONG/SHORT 동시 포지션 생성: PASS
- 동일 종목 중복 진입 차단: PASS
- 시장 국면 진입 저장: PASS
- 전략 태그 저장: PASS
- MFE/MAE mark update: PASS
- 자동 익절 청산: PASS
- 수동 청산: PASS
- 보유시간 저장: PASS
- 국면·방향·전략별 성과 저장: PASS
- 종목 재진입 쿨다운: PASS
- 상태 파일 저장 및 재로드: PASS
- 실계좌 주문 기능 부재: PASS

## Railway에서 추가 검증할 항목
- Binance 후보 스캔 실시간 응답
- 24~72시간 Auto Scan 안정성
- Railway 재배포 후 포지션 복원
- 다중 포지션 동시 TP/SL 처리
- CoinGlass 및 Telegram 일시 장애 후 복구

실계좌 자동매매 전환 검증은 포함하지 않았습니다.
