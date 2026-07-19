# A100 V116.1 DEV S58.1 Changelog

## Current Identity & Runtime Route Resolution Hotfix

- Fixed S57.8 identity audit treating the S58 `/version` handler as a regression.
- Updated `/verifyall` to evaluate the current S58.1 route set.
- Updated Regression Guard to use the current identity audit.
- Runtime Link Matrix now resolves Virtual and compatibility routes.
- `/evidence`, `/snapshot`, and `/outcome` are no longer reported as physically
  disconnected when their proven compatibility diagnostic path exists.
- Command certification remains evidence-conservative: PARTIAL is not promoted
  to PASS without runtime execution evidence.
- Registry remains 341/341.
