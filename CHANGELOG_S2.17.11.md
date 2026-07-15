# A100 V116.0 LTS-S2.17.11

## Persistent Restore Final & Runtime History
- Added checksum-verified compressed binary certification snapshot persistence.
- Added atomic current/previous snapshot rotation and rollback restore.
- Preserved legacy JSON restore as a compatibility fallback.
- Added bounded 1h/6h/24h/72h runtime history summaries to Release Gate and Version Audit.
- Kept non-blocking Telegram request paths, TTL cache, proactive refresh, Schema 1, Paper 20, Shadow 60 and Live OFF.
- No new Telegram command was added; registry remains 341.
