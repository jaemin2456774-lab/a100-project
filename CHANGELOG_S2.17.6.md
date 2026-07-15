# A100 V116.0 LTS-S2.17.6
## Preflight Diagnostics & Cache Single-Flight

- Replaced inherited legacy preflight aggregation with authoritative current-version checks only.
- Added explicit PASS/WARN/FAIL preflight diagnostics and names/details for every check.
- Prevented false `Startup Preflight FAILED · Failed Checks 3` caused by superseded handler identity checks.
- Added single-flight snapshot refresh lock so concurrent `/releasegate` and `/versionaudit` requests share one build.
- Added stale-cache fallback if a refresh fails.
- Added cache source, age, and TTL to Version Audit.
- Preserved Schema 1, Paper 20, Shadow 60, Live OFF, Registry 341, and non-blocking command paths.
