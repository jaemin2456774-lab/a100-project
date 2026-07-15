# A100 V116.0-LTS-S2.18.2
## Baseline Contract & Regression Recovery

- No new trading feature.
- No score boost, threshold relaxation or synthetic PASS.
- Preserves the exact S2.18.1 gate matrix and fast-context formulas.
- Adds permanent A100 baseline contract and protected feature inventory.
- Adds formula fingerprint checks for authoritative gate and score-input paths.
- Adds build regression tests for 341 commands, safety invariants, active handlers and single executable entrypoint.
- Keeps S2.18.1 immutable snapshot state and cache prewarm.
- Keeps S2.17.29 clean stabilization principles as recovery reference.
- Clarifies that a changed Snapshot ID may legitimately change scores; identical snapshot identity must remain frozen.
