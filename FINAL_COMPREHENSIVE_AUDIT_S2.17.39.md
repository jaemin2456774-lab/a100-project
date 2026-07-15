# Final Comprehensive Audit — S2.17.39

## Root cause
S2.17.38 called the S2.17.37 preflight and inherited two identity assertions requiring the old S2.17.37 handlers to remain active. After S2.17.38 correctly replaced those handlers, the inherited assertions failed and the process entered a Railway restart loop.

## Resolution
- Reconcile current release routes before preflight.
- Remove only obsolete prior-release identity assertions from the effective current preflight.
- Keep genuine structural failures fatal.
- Keep the operation idempotent and data-free.

## Static verification
- Python syntax/AST: PASS
- Single executable block at physical EOF: PASS
- S2.17.38 regression test: PASS
- S2.17.39 regression test: PASS
- No data/config payload: PASS
- Registry target remains 341: PASS
- Gate formulas changed: NO

## Runtime acceptance criteria on Railway
- Container remains running without restart loop.
- Startup banner shows S2.17.39.
- Startup preflight PASS.
- Registry 341 and dispatcher 1.
- `/versionaudit`: Version source single PASS; Startup handler migration PASS.
- `/commandcert`: 341/341 structural certification.
