# A100 V116.0 LTS-S2.17.15

## Runtime Evidence Consistency & Unified Metrics Final

- Runtime score, correlation, 1h/6h/24h/72h windows and audit now read one canonical Runtime Evidence DB source.
- Added de-duplication, UTC ordering and bounded clock-skew handling so longer windows cannot contain fewer samples than shorter windows.
- Added evidence-derived Runtime Score V3 while keeping all mandatory Release Gate thresholds authoritative.
- Added a 60-second derived-view cache so `/releasegate` and `/versionaudit` share the same Snapshot ID, evidence minute and Unified Hash.
- Corrected cache arithmetic by showing Overall Hit Rate and Operational Hit Rate separately; cold-start misses are explicitly identified.
- Added persisted Build/Restore operation timing rather than reporting unmeasured builds as successful builds.
- Added Runtime Evidence Consistency Audit for canonical source, monotonic windows, cache arithmetic and shared output source.
- Preserved non-blocking Telegram handlers, TTL cache, single-flight refresh, proactive refresh, persistent restore and rollback.
- Schema 1, Paper 20, Shadow 60, Live Trading OFF, Feature Freeze and Release Freeze are unchanged.
