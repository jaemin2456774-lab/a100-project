# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.2
- Build ID: V118.0-RC3.12.2-20260723-HEAVY-STAGE-BUDGET-RETRY-STATE-01
- Base: latest deployed V118.0-RC3.12.1 ZIP supplied by the user

## Stabilization work
- Fixed queued Heavy commands showing `EMPTY`; queued commands now show `WAITING`.
- Added visible stages: WAITING → BUILDING_RENDER → COMMITTING → READY.
- Added command-specific render leases:
  - Sniper 180s
  - Paper 90s
  - Shadow 120s
- Added bounded automatic retry: one retry after backoff.
- Removed immediate endless retry loops.
- Cold boot eagerly builds Sniper only; Paper and Shadow build lazily on request.
- Status output exposes lease age/budget, queue position, and retry attempt.
- RC3.12.1 symbol retry/quarantine protections remain intact.
- Registry, Certification, Ledger, Learning, gates, weights, and roadmap unchanged.

## Mandatory workflow
- Every future modification starts from the latest deployed ZIP as SSOT.
- MOBILE FLAT remains the default.
