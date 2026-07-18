# A100 V116.1 DEV S44.2 Changelog

## Common Import Dependency Stability Hotfix

Base: A100 V116.1 DEV S44.1

### Fixed
- Added missing global `copy` import used by S37 cache, S38 evidence review, S40 watchdog, and S41 resource worker paths.
- Promoted `gc` to the common import section for deterministic worker availability.
- Added startup dependency audit for `Path`, `copy.deepcopy`, `gc.collect`, and `json.loads`.
- Updated runtime/version/log identity to S44.2.

### Preserved
- S44 memory pressure containment and certification continuity state.
- Registry 341, Schema 1, Paper 20, Shadow 60, Live Trading OFF.
- No Runtime, Final AI, Consensus, Release Gate, order, or certification mutation.
