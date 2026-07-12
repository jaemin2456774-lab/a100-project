# A100 V91.8 Scenario Decision Engine

## Added
- Five-way scenario generation: pullback continuation, immediate breakout, range/accumulation, fakeout, invalidation.
- Scenario probability normalization to 100%.
- Entry-state classification: WATCH, READY, TRIGGERED, LATE, INVALID.
- Price plan: entry range, breakout trigger, target 1/2, invalidation, estimated time window.
- `/scenario <symbol>` and `/scenario_top` Telegram commands.
- Scenario cache (`PAPER_SCENARIO_CACHE_SECONDS`, default 120 seconds) to avoid repeated heavy scans.

## Preserved
- State file: `a100_v91_paper_state.json`
- State schema: `1`
- Existing Paper, Shadow, learning, expectancy, lifecycle, adaptive strategy, Meta, and pattern-similarity history.
- Existing `/decision` command behavior.
- Paper-only safety; no live-order execution path.

## Command registry
- V91.7 baseline: 133 commands
- V91.8: 135 commands
- `/help` and `/commands V91` synchronized.
