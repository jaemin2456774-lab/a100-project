# A100 V116.0 LTS S2.17.43
## Unified Summary UI & Runtime Trend Polish

- `/coach`와 5개 Analyzer를 기본 Summary / 선택 Detail 구조로 통일
- `detail` 인수로 전체 우선조치 표시
- Priority를 CRITICAL / WARNING / WATCH / PASS로 표준화
- Gate 진행률 막대와 남은 격차 표시 통일
- `/runtimehealth`에 uptime, cycle, evidence latency, conservative trend 추가
- `/ltsreadiness`에 72H 진행률과 증거 기반 Trend 표시
- Registry 341, Runtime First, Strict Read Only, Gate 공식/임계값 유지
