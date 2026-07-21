# A100 V117.0 RC6 릴리스 노트

## 목표
명령 조회와 Safe QA Batch의 체감 지연을 줄이면서, Batch 종료 시 강한 SSOT/Provenance 검증은 유지합니다.

## 변경
- `/commandcert`, `/commandmatrix`, status 조회에 30초 bounded cache 적용
- 조회 시 341개 Projection/Queue 강제 재계산 제거
- Probe 전 중복 ledger refresh 제거
- 일반 명령 6초, slow 명령 10초 soft timeout
- TIMEOUT/SLOW 명령은 slow queue로 이관하고 다음 명령 계속 실행
- Batch 완료 시에만 캐시 무효화 및 강한 reconciliation 수행
- 완료 Runner의 오래된 heartbeat를 `N/A (completed)`로 표시
- status/summary 출력에 render latency 표시

## 안전 원칙
Registry 341/341, Runtime First, Strict Read Only, Mutation Firewall, Historical isolation, Live Trading OFF를 유지합니다.
