# A100 V116.0 LTS S2.17.27

## Fixed
- Replaced `/runtimehealth` legacy full runtime/state scan with a read-only shared-snapshot fast path.
- Removed user-command waiting on Release Gate background work and shared locks.
- Replaced `/releasegate` background reply task with one inline cached response.
- Added explicit command-isolation diagnostics.
- Finalized output-boundary version normalization to S2.17.27 for legacy RC/S2 cached views.

## Preserved
- Telegram commands: 341
- Schema: 1
- Paper: 20
- Shadow: 60
- Live trading: OFF
- Existing `/data`, environment variables and configuration are untouched.
