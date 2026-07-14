# A100 V116.0 LTS-S2.11.1 Hotfix

## Fixed
- Corrected startup `NameError` caused by instantiating undefined `V1160VersionManager`.
- Reused the existing immutable `_V1160RC4923VersionManager` single-source version manager.
- Removed unsupported `baseline` constructor argument.

## Preserved
- S2.11 Final Polish Intelligence features.
- Schema 1, Paper 20, Shadow 60, Live Trading OFF.
- Registry/handler/runtime/output route target 341/341.
- No data migration and no schema change.
