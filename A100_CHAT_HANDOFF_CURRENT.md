# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.3
- Build ID: V118.0-RC3.13.3-20260724-DEGRADED-COMMIT-RAW-RECOVERY-01
- Base: latest deployed RC3.13.2 ZIP supplied by user

## Stabilization
- FILTERED_SCAN timeout can no longer leave Sniper waiting indefinitely.
- On first-boot timeout, an explicitly degraded EMPTY generation is committed.
- If a verified cache already exists, it is reused without overwrite.
- Raw fallback moved to an independent single-flight recovery worker.
- Producer cycle returns immediately after commit/reuse and hands off Sniper.
- Raw recovery later commits improved data and triggers a second safe handoff.
- Timeout remains visible as degraded evidence; no synthetic candidate is created.
- Producer/Snapshot decoupling, async persistence, worker guards and read views remain.
- Registry 341/341, Runtime First, Strict Read Only, Live OFF, Ledger,
  Certification, Learning, gates, thresholds, weights and roadmap unchanged.
- MOBILE FLAT.
