# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.1
- Build ID: V118.0-RC3.12.1-20260723-SNAPSHOT-LEASE-SYMBOL-RESOLVER-STABILITY-01
- Base: latest deployed V118.0-RC3.12.0 ZIP supplied by the user

## Stabilization work
- Added timeout-bounded Heavy Snapshot leases.
- A stale render thread cannot commit after its lease expires.
- Scheduler automatically recovers stale RUNNING leases.
- Snapshot is atomically swapped only after a successful complete render.
- Generation increments and age resets to zero on commit.
- Added price retry and authoritative Binance symbol refresh.
- Invalid/delisted symbols are quarantined.
- Temporary API failures preserve Shadow positions as PRICE_UNAVAILABLE instead
  of recording strategy/runtime failures.
- No roadmap, threshold, weight, certification, ledger, learning, or gate change.

## Mandatory workflow
- Every future modification starts from the latest deployed ZIP as SSOT.
- MOBILE FLAT remains the default package format.
