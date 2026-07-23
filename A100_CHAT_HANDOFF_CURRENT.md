# CHAT HANDOFF — CURRENT

## Current baseline
- V118.0-RC3.13.7
- Build ID: V118.0-RC3.13.7-20260724-ULTIMATE-FASTPATH-COVERAGE-READER-SYNC-01
- Base: latest deployed RC3.13.6 ZIP supplied by user

## Fixes
- /ultimate moved from the 12-second legacy dispatcher to an exclusive Heavy Snapshot path.
- /ultimate consumes the existing Filtered View and performs no network scan in isolated rendering.
- Coverage Audit now classifies only dropped rows and enforces:
  Classified + Unclassified = Dropped.
- Reader telemetry exposes pending Producer generation delta.
- Ultimate joins Shared View fanout with Sniper/Paper/Shadow.
- Existing Runtime First, Strict Read Only, Registry 341/341, Live OFF,
  Raw Recovery background, Mutation Firewall, Async Persistence and roadmap remain.
- MOBILE FLAT.
