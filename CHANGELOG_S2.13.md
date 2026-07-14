# A100 V116.0 LTS-S2.13 Final Calibration Activation

## Fixed
- Corrected the executable-order defect that caused the S2.11 `__main__` block to run before S2.12 definitions and command-route overrides were loaded.
- Moved the sole startup block to the physical end of `main.py`.
- Updated the active build identity to `A100 V116.0-LTS-S2.13 FINAL CALIBRATION ACTIVATION`.

## Activated
- Raw Runtime Score / Calibrated Runtime Score output.
- Authoritative evidence calibration.
- Calibrated Release Gate forecast and 24-hour forecast output.
- S2.13 command routes for `/version`, `/status`, `/runtimehealth`, `/dashboard`, and `/releasegate`.

## Preserved
- Schema 1, Paper 20, Shadow 60, Live Trading OFF.
- Existing 341-command registry and mandatory release-gate authority.
- Existing data and storage paths.
