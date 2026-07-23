# ACTIVE SPRINT

## Version
V118.0 RC3.12.x — Runtime stabilization.

## Current objectives
- Complete Heavy state visibility and prevent retry loops.
- Give Sniper enough bounded time to complete its real renderer.
- Keep Paper/Shadow from competing during cold boot.
- Preserve Snapshot atomic commit and lease recovery.
- Preserve symbol resolver and quarantine stability.
- No roadmap change.

## Exit criteria
- Registry 341/341.
- Sniper state progresses WAITING/BUILDING_RENDER/COMMITTING/READY.
- Paper and Shadow show WAITING when queued, never EMPTY.
- Sniper lease budget displays 180s.
- Timeout retries at most once automatically.
- No endless IDLE → queued → timeout loop.
- Successful Snapshot logs generation increment and age=0.
- MOBILE FLAT maintained.
