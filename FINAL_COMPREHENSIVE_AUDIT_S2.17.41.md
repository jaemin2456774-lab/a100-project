# Final Comprehensive Audit — S2.17.41

## Defect fixed
S2.17.40 invoked the S2.17.39 base preflight after installing S2.17.40 handlers. The base preflight could restore S2.17.39 handlers, causing false failures for version, versionaudit and commandcert routes.

## Resolution
S2.17.41 performs a second idempotent current-version reconciliation after the inherited audit, then certifies the final registry state.

## Verification
- Python syntax / AST: PASS
- S2.17.41 static regression: PASS
- Single executable block at physical EOF: PASS
- Data/config included: NONE
- Registry target: 341
- Gate formulas: UNCHANGED
