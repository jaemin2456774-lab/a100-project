# ACTIVE SPRINT

## Version
V118.0 RC3.12.x — Heavy Snapshot runtime-path stabilization.

## Current objectives
- Remove exchange/network waits from isolated Snapshot rendering.
- Build Sniper from the existing Runtime scan cache only.
- Keep stale/empty evidence explicitly labeled.
- Preserve authoritative normal runtime scan behavior.
- Complete Snapshot commit within the bounded lease.

## Exit criteria
- Registry 341/341.
- Railway logs `SNAPSHOT SCAN FASTPATH ... network=NONE`.
- `/sniper` no longer remains in select()/async wait for 180 seconds.
- Snapshot either becomes FRESH or honestly reports NO_ANALYSIS_ROWS.
- Commit Verify PASS after successful generation.
- No synthetic evidence, threshold, weight, gate, or order mutation.
- MOBILE FLAT maintained.
