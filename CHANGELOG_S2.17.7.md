# A100 V116.0 LTS-S2.17.7
## Snapshot TTL Cache Observability Final Stabilization

- Snapshot TTL 300초 내 `/releasegate`와 `/versionaudit`가 동일 immutable snapshot을 재사용합니다.
- Snapshot Source, Age, TTL, Expires In을 출력합니다.
- Cache Hit/Miss, Hit Rate, Refresh, Stale Fallback 통계를 추가했습니다.
- Cache Miss 원인을 startup/empty/ttl_expired/forced/refresh_error로 표시합니다.
- 동시 Cache Miss는 Single-Flight Lock으로 1회만 갱신합니다.
- 갱신 실패 시 기존 정상 Snapshot을 stale fallback으로 재사용합니다.
- `/releasegate`와 `/versionaudit`의 Snapshot ID 및 Unified Hash 동기화를 유지합니다.
- Schema 1, Paper 20, Shadow 60, Live Trading OFF를 유지합니다.
