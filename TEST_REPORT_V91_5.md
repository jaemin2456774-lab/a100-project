# A100 V91.5 TEST REPORT

## 통과 항목

- Python 문법 컴파일
- 모듈 import
- V91 preflight
- 전체 명령 126개 등록
- 기존 Paper LONG/SHORT 진입·청산
- 중복 진입 차단
- 재진입 쿨다운
- MFE·MAE 갱신
- Shadow 생성·익절 청산
- Shadow 생애주기 PARTIAL/TRAILING 이벤트 저장
- Self-Learning 기존 보정 유지
- 패턴 통계 생성
- 베이지안 보정 승률 범위 확인
- 기대값 및 추천등급 생성
- 신규 콜백 3개 등록

## 미검증 항목

- Railway 장시간 24시간 이상 실행
- 실제 Binance 네트워크 지연·429·5xx 상황
- Railway 재배포 중 Volume 동시성
- Telegram 실환경 메시지 길이 제한

위 항목은 실제 Railway 배포 후 관찰이 필요합니다.
