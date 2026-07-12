# CHANGELOG V91.4

## Added
- Fast Learning Shadow Trading Engine
- WATCH/READY/ENTRY 단계별 독립 가상 시나리오
- Shadow TP/SL/TIME_STOP 자동 청산
- Shadow MFE/MAE·시장국면·전략·신뢰도 저장
- Shadow 전용 성과 집계 및 Telegram 명령 3개

## Changed
- 기본 Paper 최대 포지션 10 → 15
- 기본 LONG/SHORT 한도 6 → 9
- 기본 재진입 쿨다운 60분 → 30분
- 후보 감시 20 → 40
- 스캔 주기 300초 → 120초
- 전체 Telegram 명령 120 → 123

## Safety
- Shadow 포지션은 실제 Paper 노출/손실한도/포지션 수에 미포함
- 실전형 Paper와 Shadow 데이터 분리
- 실계좌 주문 기능 없음
- `/arkm`, `/syn`, `/sent`, `/futures` 제외 유지
