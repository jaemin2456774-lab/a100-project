# A100 V116.1 DEV S59.7.5.3

## Fixed
- Canonical Matrix command extraction now accepts both `command` and `name` schema fields.
- Registry reconciliation runs after all current route replacements.
- Commands outside the measured 341-command matrix are removed without synthesizing replacements.
- `/crossengineaudit` now awaits the existing `_v1161_s5973_drift_classification()` function.
- Removed reference to undefined `_v1161_s5974_cross_engine_drift`.
- Current labels unified to S59.7.5.3 for version, drift, replay, and RC predictor outputs.

## Preserved
- Runtime First
- Strict Read Only
- Registry target 341
- Schema 1 / Paper 20 / Shadow 60 / Live OFF
- Synthetic Completion OFF
- Gate formula unchanged
- Existing Runtime and Learning data preserved
