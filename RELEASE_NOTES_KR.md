# A100 V116.2 RC2.4.2 릴리스 노트

- `/commandcert` 인자 전달 복구: `context.args`와 원문 메시지 이중 파싱
- `batch N run`, `autorun`, `status`, `stop`, `full`, `report` 모드 분리
- Runner 현재 Batch/명령/heartbeat/누적 결과/종료 상태 보존
- Batch 완료 후 `COMPLETED`, 전체 완료 후 `COMPLETED`, 중지 요청 시 `STOP_REQUESTED/STOPPED` 표시
- Bootstrap/Route 초기화와 현재 버전 배너의 프로세스당 1회 실행 보장
- Registry 341/341, Runtime First, Strict Read Only 유지
- Gate, Threshold, Learning, Paper, Live 주문 경로 변경 없음
