# A100 V116.2 RC2.4.8 릴리스 노트

## 변경 사항
- Safe QA Probe마다 immutable `qa_probe_id` 부여
- Historical anomaly를 신규 ID 단위로 비교
- 증가 원인을 `QA_CAUSED`, `BACKGROUND_CONCURRENT`, `UNKNOWN`으로 분리
- `/aidashboard` 및 기존 mutation-risk 명령 영속 격리 유지
- Batch reconciliation을 global counter가 아닌 provenance event 기준으로 판정
- Version Audit에서 QA와 Background 파이프라인을 별도 인증

## 불변 사항
- Historical 데이터 삭제/정규화 없음
- Synthetic completion 없음
- Gate, Threshold, 주문 및 Live 경로 변경 없음
- Registry 341/341 유지
