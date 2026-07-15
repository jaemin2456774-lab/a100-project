# A100 V116.0 LTS-S2.17.5
## Non-Blocking Version Audit Cache Recovery

- `/versionaudit` 즉시 ACK 후 백그라운드 결과 전송
- Telegram 120초 dispatcher timeout 경로 제거
- Version Audit 요청 경로에서 legacy full preflight 및 341개 runtime probe 실행 금지
- Immutable certification snapshot cache 우선 사용
- 캐시 미준비 시 백그라운드에서만 복구 생성
- Snapshot Source / Age 표시
- S2.17.5 최종 버전 및 핸들러 재바인딩
- Schema 1, Paper 20, Shadow 60, Live OFF 유지
