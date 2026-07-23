# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.9
- Build ID: V118.0-RC3.13.9-20260724-READER-ATTACH-IDEMPOTENT-QUEUE-PROMOTION-01
- Base: latest deployed RC3.13.8 ZIP supplied by user

## RC3.13.9 fixes
- Reader attachment is idempotent per Producer generation.
- VIEW_READY cannot regress to ATTACH_START/OK for the same generation.
- A direct user request can promote an already queued Heavy command.
- Ultimate is no longer eagerly queued by Producer/refinement; it is on-demand priority.
- Existing usable snapshot is returned immediately as LAST-GOOD-WHILE-REFRESH.
- Shared-view absence is reported as WAITING_FOR_SHARED_VIEW, not false ATTACH_OK.
- Sniper/Ultimate publish can use verified CACHE_REUSE or last-good evidence.
- Pending telemetry shows delta and target generation.

## Preserved
- Runtime First / Strict Read Only / Registry 341/341 / Live OFF.
- Raw-first Producer, background Filter Refinement, Last-Good retention.
- Filtered Cache, Shared View, Coverage Sum PASS, Mutation Firewall,
  Async Persistence, Learning/Ledger/Gates/Thresholds/Weights.
- MOBILE FLAT.

## Next measured target
- Shadow Dashboard projection cache: remove 26–30s Cache MISS render path.
