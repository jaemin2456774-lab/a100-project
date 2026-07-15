# A100 V116.0 LTS-S2.17.9
## Operational Cache · Proactive Refresh · Runtime Guard

- Cold-start MISS를 운영 Cache Hit Rate에서 분리했습니다.
- Operational Requests/Hits/Misses/Hit Rate를 추가했습니다.
- TTL 만료 전에 백그라운드 Snapshot을 생성하고 기존 Snapshot을 계속 제공한 뒤 원자적으로 교체합니다.
- `/releasegate`와 `/versionaudit`는 무거운 엔진을 Telegram 요청 경로에서 실행하지 않습니다.
- Snapshot Build/Refresh 통계와 Peak Snapshot Age를 출력합니다.
- 5분 간격 장시간 인증 이력을 `/data/v1160_s2179_runtime_certification.jsonl`에 제한적으로 저장합니다.
- 이력 파일은 약 2MB 초과 시 최근 1000개 행으로 자동 축소합니다.
- Schema 1, Paper 20, Shadow 60, Live OFF, Registry 341을 유지합니다.
