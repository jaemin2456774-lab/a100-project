# ACTIVE SPRINT

## Version
V118.0 RC3.11.x — Performance and stabilization.

## Current objectives
- Preserve the verified seven-command core warmup.
- Isolate `/paper`, `/sniper`, and `/shadow` from Telegram dispatcher timeout.
- Build read-only authoritative snapshots in background.
- Serve fresh or clearly labeled stale snapshots immediately.
- Continue observed hotfixes without changing the approved roadmap.
- No unplanned product features.

## Exit criteria
- Registry 341/341.
- Core Boot Warmup READY · 7/7 · 35/35.
- `/paper`, `/sniper`, `/shadow` do not produce dispatcher TIMEOUT.
- First command receives a response within approximately 3 seconds.
- Subsequent snapshot reads are immediate.
- Snapshot source remains the existing authoritative handler.
- No certification, ledger, learning, gate, or live-trading mutation.
- MOBILE FLAT packaging maintained.
