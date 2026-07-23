# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.12.5
- Build ID: V118.0-RC3.12.5-20260723-STATE-LOAD-CACHE-HTML-SAFE-01
- Base: latest deployed RC3.12.4 ZIP supplied by user

## Stabilization work
- Added signature-aware V91 state cache using mtime_ns + file size.
- Repeated reads within the bounded TTL use a defensive deep copy.
- Successful saves refresh the cache immediately.
- State loader records READ_JSON, NORMALIZE, CACHE_HIT, READY, and failure stages.
- Slow loads log file size and per-stage elapsed times.
- Render telemetry now reports exact STATE_LOAD_* status.
- Telegram entity parse failures automatically retry as plain text.
- Existing leases, commit verification, retries, symbol resolver, Registry,
  Certification, Ledger, Learning, gates, and roadmap remain unchanged.

## Mandatory workflow
- Latest deployed ZIP is always the development SSOT.
- MOBILE FLAT remains default.
