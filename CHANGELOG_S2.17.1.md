# A100 V116.0 LTS-S2.17.1
## Startup Healthcheck Ordering Hotfix

- Removed the blocking full preflight and certification snapshot from the executable block.
- Railway health server is opened before certification warmup or learning-worker initialization.
- Heavy snapshot, evidence, memory, learning and pipeline warmup now runs in a daemon thread after startup.
- Replaced the preflight snapshot execution check with a non-blocking callable integrity check.
- Preserved all 341 commands, Schema 1, Paper 20, Shadow 60 and Live Trading OFF.
- Preserved S2.17 audit titles, shared snapshot, unified score hash and persistent 72H scheduler.
