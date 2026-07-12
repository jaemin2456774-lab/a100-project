# A100 V92.8 Command Integrity & Version Sync

## 핵심 수정
- `/papershadowstatus`, `/papershadowpositions`, `/papershadowhistory`, `/papershadowstats`를 최종 명령 레지스트리에 명시적으로 재등록
- HELP, COMMANDS, AI Decision, Dashboard, Final 출력 버전을 V92.8로 동기화
- Raw Confidence / Calibrated Confidence / Calibration Gain 표시
- 학습 진행 막대와 `평가 수/목표 수` 표시
- 시작 전 명령 레지스트리·도움말 동기화 검증 강화

## 데이터 호환
- 기존 상태 파일 `a100_v91_paper_state.json` 유지
- schema 1 유지
- Paper/Shadow/Open/Closed/Memory 데이터 보존
- 실주문 기능 없음
