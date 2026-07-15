# A100 V116.0 LTS-S2.17.8

## Cache Policy / Build Metrics / Long Runtime Guard
- TTL cache reuse is invalidated only by TTL expiry, explicit force, or registry/policy fingerprint change.
- Human-readable miss reasons replace raw codes such as stale().
- Added requests, hits, misses, hit rate, refresh/stale count, last/average build time, last refresh UTC and policy fingerprint.
- Release Gate and Version Audit remain non-blocking and share one immutable single-flight snapshot.
- Schema 1, Paper 20, Shadow 60, Live OFF and Registry 341 are preserved.
