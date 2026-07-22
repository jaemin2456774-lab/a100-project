# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.11.5
- Build ID: V118.0-RC3.11.5-20260723-HEAVY-SNAPSHOT-PERSISTENCE-SCHEDULER-01
- Base: V118.0-RC3.11.4

## Current sprint work
- Heavy snapshots persist to Railway `/data`.
- Restores `/paper`, `/sniper`, and `/shadow` output after restart.
- Heavy refresh concurrency is one to avoid DB/disk contention.
- User-requested refresh receives queue priority.
- TTL: paper 60s, sniper 120s, shadow 300s.
- Certification, Registry, Ledger, Learning, Trading Gate, and roadmap unchanged.

## Distribution
- MOBILE FLAT
- No folder creation required
