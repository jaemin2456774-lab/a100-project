# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.7
- Build ID: V118.0-RC3.12.7-20260723-SCHEDULER-WAKE-COMMIT-STATE-MACHINE-01
- Base: latest deployed RC3.12.6 ZIP supplied by user

## Stabilization work
- Replaced Heavy Scheduler polling with threading.Event wake.
- Queue push immediately wakes the single worker.
- State flow:
  QUEUE_PUSH → WAITING → WAKE → WORKER_ASSIGNED →
  BUILDING_RUNTIME → BUILDING_RENDER → COMMITTING → VERIFY → READY.
- Added worker id, wake count, and queue push count telemetry.
- Retry requeue also wakes the worker.
- Runtime Scan Cache FastPath and all safety architecture remain unchanged.

## Mandatory workflow
- Latest deployed ZIP is the development SSOT.
- MOBILE FLAT remains default.
