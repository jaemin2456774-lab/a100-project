# A100 V116.0 LTS S2.17.44
## Unified Output & Runtime Performance Monitor

- Planner/analyzer output format unified as header → state → gauge → actions → read-only footer.
- Runtime Health now reports in-memory monitoring-window sample count, average/P95/maximum worker cycle, heartbeat P95, evidence-age P95 and freshness ratio.
- Added non-persistent 2-second runtime telemetry sampler. It reads LIVE_RUNTIME only and does not scan storage or alter evidence.
- Registry remains 341; no new command was introduced.
- Gate formulas, thresholds, Schema 1, Paper 20, Shadow 60 and Live OFF remain unchanged.
