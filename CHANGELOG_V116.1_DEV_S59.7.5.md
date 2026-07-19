# A100 V116.1 DEV S59.7.5

## Scope
Current Route Unification / Worker Truth / Replay RC Synchronization Hotfix

## Fixed
- `/versionaudit` current label/build route unified to S59.7.5.
- `/runtimehealth` old S59.2.1 output replaced with current DEV read-only health output.
- `/status` worker state now uses live runtime freshness with worker-status fallback; false STOPPED removed.
- `/releasegate` old V116.0 LTS S2.17.49 handler replaced with V116.1 DEV S59.7.5 gate output.
- `/crossengineaudit`, `/rcpreflight`, `/evidencereplay` outputs unified to S59.7.5.
- Replay truth and RC snapshot continue using the same current runtime evidence source.
- Telegram timeout retry retained.

## Command-name clarification
Registry remains exactly 341/341. No synthetic alias commands were added.
- `/crossengine` -> use `/crossengineaudit`
- `/rcpredictor` -> use `/rcpreflight`
- `/coverage` -> use `/commandmatrix` or `/coveragestatus`
- `/ledger` -> use `/ledgeraudit`

## Safety invariants
Runtime First, Strict Read Only, Schema 1, Paper 20, Shadow 60, Live OFF, Synthetic OFF, Gate Formula unchanged, existing runtime/learning data preserved.
