# A100 V117.0 RC4 릴리스 노트

## Build
- Version: V117.0-RC4
- Build ID: V117.0-RC4-20260721-CERTIFICATION-AUTOMATION-PRIORITY-PROMOTION-01

## 핵심 변경
- 기존 Safe QA Runner 위에 SSOT 기반 Certification Priority Queue 추가
- PARTIAL 명령 중 PASS에 가까운 명령을 먼저 실행
- 기존 quarantine 및 unsafe 명령 제외 정책 유지
- Batch 종료 후 Certification Projection 재계산
- 실제 PARTIAL/FAILED → PASS 상태 전환만 immutable ledger에 append
- 중간 Probe 및 단순 조회는 ledger append 없음
- `/commandcert status`에 Queue, PASS, Promotion, Projection 상태 추가

## 불변 사항
- Registry 341/341
- Runtime First / Strict Read Only
- Historical 삭제·정규화 없음
- Gate/Threshold/Order mutation 없음
- Live Trading OFF
