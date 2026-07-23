# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.6
- Build ID: V118.0-RC3.12.6-20260723-RUNTIME-SCAN-CACHE-FASTPATH-01
- Base: latest deployed RC3.12.5 ZIP supplied by user

## Stabilization work
- Heavy Snapshot rendering no longer launches Binance/exchange scans in its
  private asyncio event loop.
- Snapshot renderer consumes the latest already-produced S45 Runtime scan cache.
- Cache source is labeled FRESH, STALE, or EMPTY with age and network=NONE.
- Normal authoritative runtime/user scan paths remain unchanged.
- Empty Runtime cache returns an honest NO_ANALYSIS_ROWS/WAIT snapshot instead
  of blocking for 180 seconds.
- Corrected select()/event-loop telemetry classification to RENDER_ASYNC_WAIT.
- Explicit user retry resets exhausted automatic retry accounting.
- Preserved state cache, HTML fallback, leases, commit verification, symbol
  resolver, Registry, Certification, Ledger, Learning, gates, and roadmap.

## Mandatory workflow
- Latest deployed ZIP is always the development SSOT.
- MOBILE FLAT remains default.
