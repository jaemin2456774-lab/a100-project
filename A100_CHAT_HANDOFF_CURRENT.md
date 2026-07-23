# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.8
- Build ID: V118.0-RC3.13.8-20260724-LAST-GOOD-VIEW-RAW-FIRST-REFINEMENT-01
- Base: latest deployed RC3.13.7 ZIP supplied by user

## Resolved in RC3.13.8
- Slow FILTERED_SCAN is no longer on the authoritative first-response path.
- Existing verified Runtime cache is handed to readers immediately.
- On first boot, bounded Raw Scan runs first; Filtered Scan becomes background refinement.
- Timeout/degraded empty data never replaces a non-empty last-good analysis View.
- /ultimate and /sniper do not create FRESH empty snapshots before real evidence exists.
- Last-good View is served with explicit pending/refinement state during refresh.
- Coverage invariant, Reader generation telemetry, Shared View, Raw Recovery,
  Mutation Firewall and Async Persistence remain.

## Fixed architecture
- Runtime First / Strict Read Only / Registry 341/341 / Live OFF.
- Ledger, Certification, Learning, Gate, Threshold, Weight and roadmap unchanged.
- MOBILE FLAT.

## Next optimization
- Shadow Dashboard Cache MISS (~26–30s) must be detached from reader render.
- Add prebuilt Dashboard Projection Cache after RC3.13.8 runtime verification.
