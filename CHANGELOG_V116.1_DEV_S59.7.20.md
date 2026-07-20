# A100 V116.1 DEV S59.7.20

Build ID: `S59.7.20-20260720-SHADOW-PRODUCER-RECONNECT-ACTIVATION-AUDIT-01`

## 수정
- 후속 V110 자동 스캔 래퍼가 덮어쓴 V91.4 Shadow capture 경로 재연결
- 최종 `_v912_auto_scan_once` 실행 후 Shadow candidate capture 복구
- Paper auto-scan이 꺼져 있어도 기존 monitor worker에서 120초 이상 간격으로 Shadow producer 실행
- Candidate/WATCH/READY/ENTRY/Close/Learning Activation Audit 추가
- 후보 필터 사유 집계: 점수 미달, 중복, 쿨다운, 포지션 한도, 단계 비활성
- Shadow Health Score 및 Worker/Scan/Capture freshness 표시

## 보존
- Registry 341/341
- Runtime First / Strict Read Only
- Paper 20 / Shadow 60
- Live Trading OFF
- Gate Formula 변경 없음
- 기존 Runtime/Learning 데이터 삭제 없음
