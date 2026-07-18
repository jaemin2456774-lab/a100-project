# A100 V116.1 DEV S44.1 — Path Import Startup Crash Hotfix

Base: A100 V116.1 DEV S44

## Fixed
- Added `from pathlib import Path` before S40 recovery-history path initialization.
- Eliminates startup crash at `_V1161_S40_HISTORY_PATH=Path(V91_DATA_DIR)/...`.
- Updated visible DEV version/log labels to S44.1.

## Preserved
- S44 memory pressure containment and boot continuity logic.
- Runtime First, Evidence Only, Schema 1, Paper 20, Shadow 60, Registry 341.
- Adaptive Weight LOCKED, Consensus/Gate/Order override DISABLED, Live Trading OFF.
- Existing `/data` and certification evidence are not deleted or recomputed.
