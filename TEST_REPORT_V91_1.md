# A100 V91.1 검증 결과

## 통과
- Python `py_compile`
- AST 파싱
- requirements 설치 후 모듈 import
- V91 preflight 전체 통과
- 등록 명령 114개 확인
- UTC 일자 키 생성
- Paper 상태 원자 저장 및 재로드
- LONG 진입
- 동일 종목 중복 진입 차단
- Take Profit 자동 청산
- SHORT 진입 및 수동 청산
- 수수료·슬리피지 반영 후 손익 계산
- 열린 포지션 제거 및 청산 이력 2건 저장

## Railway에서 추가 확인 필요
- Telegram 실제 명령 응답
- Railway Volume 영속성
- 컨테이너 재시작 후 상태 복원
- Binance 실시간 가격 장시간 호출
- PostgreSQL 일시 장애 복구
- Watchdog/Paper Monitor 24시간 이상 동작
