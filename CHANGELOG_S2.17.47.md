# A100 V116.0 LTS S2.17.47
## Final Contract Integrity & Release Audit Fix

- Added an S2.17.47-native `/versionaudit` handler.
- Fixed Startup Migration verification to compare the live registry against the current release handlers.
- Removed stale `/evidence` advertising because it is not part of the frozen 341-command registry.
- Kept persisted evidence maturity available through `/ltsreadiness detail`.
- Added advertised-command contract and critical-handler identity checks.
- Preserved Registry 341, Runtime First, Strict Read Only, Evidence Worker, Schema 1, Paper 20, Shadow 60, Live OFF, and unchanged gate formulas/thresholds.
