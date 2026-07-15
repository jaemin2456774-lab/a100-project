# A100 V116.0 LTS-S2.17.14

## Evidence-Calibrated Score · Windowed History · ETA Stability

- Runtime Score를 72시간 Runtime Evidence와 보수적으로 연동했습니다.
- Mandatory Gate는 기존 권위 기준을 유지하며 보정값으로 우회되지 않습니다.
- 1h/6h/24h/72h 구간을 실제 UTC 시간창으로 독립 집계합니다.
- 각 시간창에 sample/expected, coverage, delta, UTC 범위를 표시합니다.
- Snapshot build time과 요청/Hit/Miss 누계를 `/data`에 영구 저장합니다.
- Gate ETA에 영구 EMA 상태와 변동 제한을 적용해 호출별 흔들림을 완화했습니다.
- `/releasegate`와 `/versionaudit` 비차단 처리, TTL cache, single-flight, proactive refresh를 유지합니다.
- Schema 1, Paper 20, Shadow 60, Live OFF, Registry 341을 유지합니다.
