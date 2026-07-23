# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.4
- Build ID: V118.0-RC3.12.4-20260723-RENDER-STACK-PROGRESS-TELEMETRY-01
- Base: latest deployed RC3.12.3 ZIP supplied by user

## Stabilization work
- Added observed Python stack telemetry for the Heavy renderer.
- Reports real active categories:
  RENDER_RUNTIME_SCAN / RENDER_FACTORS / RENDER_EXPLAINABILITY /
  RENDER_OUTPUT / RENDER_WAIT / RENDER_HANDLER.
- Samples the worker stack every two seconds without blocking Telegram.
- Logs active function and source line every ten seconds.
- Shows stack sample count and unchanged duration to distinguish progress from
  a true blocked call.
- Preserves RC3.12.3 commit verification, leases, bounded retry, symbol resolver,
  Registry, Certification, Ledger, Learning, gates, and roadmap.

## Mandatory workflow
- Latest deployed ZIP is the development SSOT.
- MOBILE FLAT remains default.
