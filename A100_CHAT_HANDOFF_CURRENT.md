# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.16
- Build ID: V118.0-RC3.13.16-20260724-ULTIMATE-HEAVY-RETIREMENT-FRESHNESS-SSOT-01
- Base: user-deployed RC3.13.15 ZIP

## RC3.13.16
- Ultimate Heavy Snapshot is retired on every route.
- /ultimate and /ultimate detail are bounded Runtime Read Views.
- Central heavy dispatcher blocks accidental command=ultimate requests.
- Freshness uses one SSOT timestamp from cache, producer commit, filtered view,
  and shared view.
- Cache/producer/filtered generations are audited together.
- Stage UI normalizes Korean lifecycle values to WATCH/READY/ENTRY labels.
- Result object adapter remains.

## Preserved
- Runtime First / Strict Read Only / Registry 341/341 / Live OFF.
- Sniper/Paper/Shadow Heavy paths remain unchanged.
- Output Chunk / Stable View / Reader Attach / Queue Promotion.
- Learning / Ledger / Gate / Threshold / Weight unchanged.
- MOBILE FLAT.
