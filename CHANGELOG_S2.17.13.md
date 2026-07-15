# A100 V116.0 LTS-S2.17.13

## Cache Optimizer V2 / Delta Evidence / Score Trend
- Cold-start misses are separated from operational cache hit rate.
- Overall and operational cache efficiency are displayed independently.
- Runtime evidence summaries now include score delta, average/peak memory, cache efficiency and errors for 1h/6h/24h/72h windows.
- Release Gate and Version Audit remain non-blocking and reuse the same immutable snapshot.
- Existing persistent restore, scheduler, checksum and rollback paths are preserved.
- Schema 1, Paper 20, Shadow 60, Live OFF and Registry 341 are preserved.
