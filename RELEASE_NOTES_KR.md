# A100 V118.0 RC3.6 릴리스 노트

Build ID: `V118.0-RC3.6-20260722-DEFERRED-MATRIX-RECOVERY-WARM-CACHE-STABILITY-01`

## 수정 범위

- 부팅 중 341개 전체 Certification Matrix 재계산 제거
- 메모리 Snapshot 또는 `/data/v118_matrix_snapshot.json` 재사용
- 저장 Snapshot이 없거나 오래된 경우 부팅을 막지 않고 백그라운드에서 1회 갱신
- `recovery_matrix_refresh` 동기 비용을 0ms로 제한하고 `recovery_matrix_reuse` 출처 기록
- Matrix Snapshot은 Registry 341 및 전체 Matrix 341개 조건을 만족할 때만 재사용
- 핵심 Render Cache 기본 TTL을 900초로 확대
- `/commandcert` TTL을 1800초로 확대
- Cache 진단을 `TTL_EXPIRED`, `NOT_FOUND`, `HIT`로 명확히 구분
- Cache age, remaining TTL, warm-cache 사용 여부 기록

## 유지 원칙

- Registry 341/341
- Runtime First
- Strict Read Only
- Ledger Append Only
- Live Trading OFF
- 기존 데이터 및 Railway 환경변수 호환
