# A100 V116.0 LTS-S2.17.2
## Single Health Server & Gate Diagnostics Patch

- Health server startup is now process-wide idempotent with a lock and started flag.
- Duplicate `Health server listening` and `Address already in use` logs are removed.
- Health-first, non-blocking certification warmup remains active.
- Release Gate now shows a diagnostic driver and velocity-based ETA for each mandatory gate.
- Existing Schema 1, Paper 20, Shadow 60, Live OFF, 341 commands and 72H certification state are preserved.
