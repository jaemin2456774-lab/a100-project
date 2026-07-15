# A100 V116.0 LTS S2.17.29

## Real-Time Evidence Delta & Incremental Gate Publish

- Keeps S2.17.26 architectural baseline and S2.17.28 strict read-only Telegram path.
- Removes active-output dependency on the S2.17.25 legacy version-normalization wrapper.
- Worker checks authoritative evidence every 30 seconds and publishes only when snapshot/evidence/score/gate values change.
- Adds per-gate progress, gap and real delta from the previous published evidence.
- Telegram commands perform no file scan, snapshot creation, evidence rebuild or gate calculation.
- Preserves 341 commands, Schema 1, Paper 20, Shadow 60 and Live OFF.
