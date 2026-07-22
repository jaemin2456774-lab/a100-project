# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.11.4
- Build ID: V118.0-RC3.11.4-20260723-HEAVY-COMMAND-SNAPSHOT-ISOLATION-01
- Base: V118.0-RC3.11.3.5

## Current sprint work
- Preserved the verified core performance baseline.
- Added registry-neutral heavy snapshot paths for:
  - `/paper`
  - `/sniper`
  - `/shadow`
- Legacy authoritative renderers now run in background threads.
- Telegram receives an immediate response and is never held for the old
  12-second dispatcher timeout.
- Fresh snapshots are served immediately.
- Usable stale snapshots are served while a refresh runs.
- The first request without a snapshot returns a clear preparation status.
- Certification, Ledger, Learning, Trading Gate, and roadmap remain unchanged.

## Distribution
- MOBILE FLAT
- No folder creation required
