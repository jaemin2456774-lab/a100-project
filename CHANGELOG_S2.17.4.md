# A100 V116.0 LTS-S2.17.4
## Startup Preflight & Release Gate Recovery Patch

- Removed recursive/deep legacy preflight from startup and Telegram request paths.
- Replaced startup validation with bounded authoritative checks only.
- Prevented stale S2.17 checks from blocking S2.17.3/S2.17.4 startup.
- Restored Telegram polling startup after health server readiness.
- Kept `/releasegate` immediate ACK plus background cached snapshot delivery.
- Added one-time post-start certification snapshot warmup.
- Rebound `/version` and `/versionaudit` to S2.17.4.
- Preserved Schema 1, Paper 20, Shadow 60, Live Trading OFF and Registry 341.
