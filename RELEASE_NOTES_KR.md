# A100 V116.2 RC2.3.1 릴리스 노트

## 목적
RC2 Entry Gate 인증을 마감하기 위한 READY Timeline V2, Evidence Ledger V2, QA Dashboard 및 성능 복구 패치입니다.

## 추가
- READY 진입/체류, 현재·최저·최고 점수, Score/Gap 변화, 차단 사유 변화, 종료 사유 추적
- ENTRY / NEAR_ENTRY / BLOCK / READY_HISTORY 진단 Evidence 분리
- Timeline 160건, Ledger 120건 bounded 저장
- `/papershadow`, `/papershadowstatus`, `/shadow` RC2 Final QA Dashboard
- 30초 dashboard snapshot cache와 startup read-only prewarm

## 불변
Gate 계산식, Threshold, Stage 생성, TP/SL, Shadow/Paper/Live 주문 경로, Learning/Attribution 로직은 변경하지 않습니다.
