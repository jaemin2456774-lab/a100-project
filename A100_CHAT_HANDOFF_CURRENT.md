# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.5
- Build ID: V118.0-RC3.13.5-20260724-READER-ATTACH-FANOUT-QUEUE-FAIRNESS-01
- Base: latest deployed RC3.13.4 ZIP supplied by user

## Stabilization
- Verified Runtime generation is attached to Sniper, Paper and Shadow readers.
- Reader states: READER_ATTACH_START → READER_ATTACH_OK → VIEW_SELECTED → VIEW_READY.
- Sniper READY fans out Paper and Shadow exactly once per producer generation.
- Repeated Producer cycles no longer requeue the same Sniper generation.
- Paper/Shadow use normal-priority fanout, preventing priority starvation.
- Existing valid reader views are reused while the producer refreshes.
- Render mutation firewall, async persistence, raw recovery and all fixed
  architecture/roadmap constraints remain unchanged.
- MOBILE FLAT.
