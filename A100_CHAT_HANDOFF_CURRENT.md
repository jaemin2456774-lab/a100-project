# CHAT HANDOFF — CURRENT

## Authoritative baseline
- V118.0-RC3.13.2
- Build ID: V118.0-RC3.13.2-20260724-PRODUCER-DECOUPLED-SNAPSHOT-GATE-01
- Base: latest deployed RC3.13.1 ZIP supplied by user

## Stabilization
- Sniper Heavy Render never starts while Runtime Producer is incomplete.
- Producer and Snapshot are fully decoupled.
- Verified Producer completion hands one Sniper job to the Heavy queue.
- Existing verified Sniper Snapshot remains readable during producer refresh.
- FILTERED_SCAN no longer causes Sniper RENDER_ASYNC_WAIT.
- Paper/Shadow are not queued behind an unproductive Sniper render.
- Async persistence, worker guards, bounded producer stages and read views remain.
- Registry 341/341, Runtime First, Strict Read Only, Live OFF, Ledger,
  Certification, Learning, gates, thresholds, weights and roadmap unchanged.
- MOBILE FLAT.
