# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.10
- Build ID: V118.0-RC3.13.10-20260724-OUTPUT-CHUNK-STABLE-VIEW-EMPTY-AUDIT-01
- Base: latest deployed RC3.13.9 ZIP supplied by user

## RC3.13.10 fixes
- Telegram output is split into bounded 3500-character pages.
- Each page has independent HTML-safe fallback and retry.
- /ultimate defaults to compact Top-1 output; /ultimate detail remains full.
- Filtered View ID is stable for identical generation/content.
- Empty Views are reusable cache HITs and no longer generate repeated IDs/MISS.
- Coverage Audit now reports Other and guarantees:
  Classified + Other + Unclassified = Dropped.
- Message-too-long BadRequest is prevented before Telegram send.

## Preserved
- Runtime First / Strict Read Only / Registry 341/341 / Live OFF.
- Reader Attach idempotency, Queue Promotion, Last-Good, Raw-first,
  Background Refinement, Shared View, Dashboard Cache, Mutation Firewall.
- Ledger / Learning / Gate / Threshold / Weight unchanged.
- MOBILE FLAT.
