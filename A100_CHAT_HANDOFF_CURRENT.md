# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.11.3.4
- Build ID: V118.0-RC3.11.3.4-20260723-LIVE-PERFORMANCE-VERSION-WARMUP-STATE-HOTFIX-01
- Base: V118.0-RC3.11.3.3

## Hotfix
- `/performance` was cached while Boot Warmup was still RUNNING, so the stale
  RUNNING/0/0 screen was served for the full cache TTL.
- `/performance` is now a live non-cached diagnostic rendered off the main loop.
- `/version` was missing from the isolated warmup renderer and is now included.
- Boot warmup now caches 7 stable commands and records 35 real lookup samples.
- Any stale performance cache is removed when warmup completes.

## Unchanged
- Registry 341/341
- PASS 56 / PARTIAL 285 / FAILED 0
- Runtime First / Strict Read Only / Live Trading OFF
- Ledger, Learning, Trading Gate, and locked roadmap

## Distribution
- MOBILE FLAT
- No folder creation required
