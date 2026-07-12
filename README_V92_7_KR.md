# A100 V92.7 Calibrated Learning & Shadow Command Fix

## 핵심 개선
- `/papershadowstatus` 등록 누락 수정
- `/papershadowhistory`, `/papershadowstats` 추가
- `/help`, `/commands V92`와 실제 콜백 동기화
- 학습 표본 기반 Confidence Calibration 추가
- 평가 20건 전 Sample Guard: Confidence 보정폭 ±2% 제한
- `/learningstatus`에 진행 막대, 최근 24시간, 보정 신뢰도 표시

## 데이터 호환
- 기존 상태 파일 `a100_v91_paper_state.json` 유지
- schema 1 유지
- 기존 OPEN/청산/Memory/Shadow 데이터 보존
- 신규 API 스캔 및 실주문 경로 없음
