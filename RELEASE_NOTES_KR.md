# A100 V118.0 RC3 릴리스 노트

Build ID: `V118.0-RC3-20260722-QA-PROVENANCE-PERFORMANCE-SAMPLE-STATIC-FASTPATH-BOOT-PHASE-01`

## 수정 사항

- 공식 QA provenance를 실패 원인에서 분리하고 격리된 검수 이력으로 표시
- Background/Unknown growth만 Historical Integrity 실패 조건으로 유지
- `/versionaudit`의 `QA Provenance Isolated` 검증 추가
- 성능 측정에서 Telegram 전송 시간을 제외하고 계산·렌더링 시간 중심으로 기록
- 샘플 0건은 `NOT MEASURED`, 최소 샘플 미만은 `MEASURING`, 이후 P95 기준 `PASS/FAIL`
- Samples, Cache Hits/Misses, 최소 샘플 기준을 `/performance`에 표시
- `/version`, `/buildinfo` 정적 Fast Path 적용
- `/commandcert`, `/commandmatrix`, `/trustgate` Projection Hash Render Cache 유지
- `/trustgate`는 캐시 HIT 시 Trust 재계산을 건너뜀
- BootManager가 identity → registry → baseline → routes → guard → recovery 순서로 단일 실행
- Boot phase별 소요시간을 `/buildinfo`에 표시
- Registry 341/341, Strict Read Only, Live Trading OFF 유지

## 배포 판정

RC3는 RC2에서 확인된 QA provenance 오판정, 성능 샘플 판정 부재, 중복 Boot 경로를 수정한 검수 후보입니다.
