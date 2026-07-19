# A100 V116.1 DEV S59.7.5.1

Corrective hotfix for Railway findings after S59.7.5.

## Fixed
- Restores the certified 341-command name baseline by removing three unintended post-baseline additions.
- Synchronizes both V90_COMMAND_REGISTRY and _V1161_S571_VIRTUAL_ROUTES.
- Routes /releasegate to the current DEV handler instead of the legacy V116.0 LTS handler.
- Makes /commandmatrix tolerant of heterogeneous row schemas and removes KeyError: status.
- Unifies /versionaudit, /runtimehealth and /status labels to S59.7.5.1.
- Preserves Runtime First, Strict Read Only, Schema 1, Paper 20, Shadow 60, Live OFF and Synthetic OFF.

## Important
- /ledgeraudit is not added because it is not part of the certified 341-command baseline.
- Ledger health remains represented by /rcpreflight and runtime evidence/replay outputs.
