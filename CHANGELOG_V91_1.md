# V91.1 변경사항

- `datetime` 전역 import 누락 수정
- `_v91_today()`를 `time.gmtime()` 기반으로 변경
- V91 preflight에 UTC 날짜 형식 및 Paper 핵심 함수 검사 추가
- Paper LONG/SHORT 진입·중복 차단·TP 청산·수동 청산·상태 복원 오프라인 테스트 통과
- Python compile/AST/import/preflight 테스트 통과
- 기존 명령 수 114개 유지
- 실계좌 주문 기능 없음
