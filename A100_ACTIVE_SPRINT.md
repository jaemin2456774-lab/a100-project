# ACTIVE SPRINT

## Version
V118.0 RC3.12.x — Runtime stabilization.

## Current objectives
- Eliminate Snapshot RUNNING deadlocks.
- Guarantee atomic Snapshot swap and generation progression.
- Recover stale leases automatically.
- Separate invalid symbols from temporary price API failures.
- Preserve Shadow positions during temporary price unavailability.
- Keep the approved roadmap unchanged.

## Exit criteria
- Registry 341/341.
- No indefinitely stuck `Refresh RUNNING`.
- Lease timeout produces RECOVERED/FAILED evidence and releases the scheduler.
- Successful refresh logs generation increment and age=0.
- Invalid symbols are quarantined.
- Temporary price failures do not become V88 strategy errors.
- MOBILE FLAT maintained.
