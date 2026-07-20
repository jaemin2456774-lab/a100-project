# A100 V116.2 RC1 통합 릴리스

## 통합 범위
S59.7.15~S59.7.22의 QA Console, Learning Evidence, Shared Snapshot, Shadow Producer, Symbol Quarantine, Entry Trace 변경을 하나의 기준본으로 통합했습니다.

## RC1 핵심
- Shadow Current Scan과 Active Queue 분리
- ENTRY Gate Current/Active 상태 동시 표시
- Shadow Attribution, Review, Accuracy 정합성 감사
- Shadow Consistency Score
- 격리 데이터와 시스템 오류 분리
- Registry 341/341, Runtime First, Strict Read Only 유지
- Live/Gate/Threshold 변경 없음

## 이후 운영
작은 수정은 develop에서 누적하고 QA 통과 시에만 RC2 또는 Stable ZIP을 생성합니다.
