# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.8
- Build ID: V118.0-RC3.12.8-20260723-WORKER-ENTRY-GUARD-SELF-HEAL-01
- Base: latest deployed RC3.12.7 ZIP supplied by user

## Stabilization work
- Added worker-thread alive detection and automatic restart.
- `_WORKER_STARTED` can no longer hide a dead worker thread.
- Added guarded QUEUE_POP and WORKER_ENTRY boundaries.
- Any entry exception is recorded, state is released, and the worker continues.
- Added worker heartbeat, restart count, and last-error telemetry.
- Reset stale per-command stage telemetry when a new queue request is accepted.
- Existing Event wake, Runtime Scan Cache FastPath, leases, commit verification,
  state cache, HTML fallback, symbol resolver, Registry, Certification, Ledger,
  Learning, gates, and roadmap remain unchanged.

## Mandatory workflow
- Latest deployed ZIP is always the development SSOT.
- MOBILE FLAT remains default.
