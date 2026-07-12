# A100 V91.4 Test Report

## 정적 검사
- Python compile: PASS
- AST/import smoke test: PASS
- V91 preflight: PASS
- command registry: 123
- 신규 callback 3개: PASS
- 제외 명령 미등록: PASS
- 실계좌 주문 함수 부재: PASS

## Paper 회귀 테스트
- LONG/SHORT 진입: PASS
- 중복 진입 차단: PASS
- MFE/MAE 업데이트: PASS
- 자동 TAKE_PROFIT: PASS
- 수동 청산: PASS
- 상태 저장·복원: PASS
- 재진입 쿨다운: PASS
- Self-Learning 점수 보정 상한: PASS

## Shadow 테스트
- Shadow 포지션 생성: PASS
- 실제 Paper 포지션 한도 미소모: PASS
- TP 자동 청산: PASS
- Shadow 청산 기록 저장: PASS
- Shadow performance 집계: PASS
- WATCH/READY/ENTRY 분리 키: PASS

## 배포 후 확인 필요
- Railway 24시간 장시간 동작
- Binance API 429 및 지연 여부
- Shadow 30→60→100 단계 확장 시 CPU/메모리
- Railway 재배포 후 Shadow 상태 복원
