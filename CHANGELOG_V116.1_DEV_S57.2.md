# A100 V116.1 DEV S57.2 Changelog

## Version
- A100 V116.1-DEV-S57.2
- Build ID: S57.2-20260719-VERSION-RENDERER-SINGLE-SOURCE-01

## Fixed
- `/version` registry route now resolves to `version1161devs572_cmd`.
- `/status` now preserves live LTS metrics while normalizing runtime identity through the S57.2 single source.
- `/runtimehealth` now preserves certification metrics while normalizing runtime identity through the S57.2 single source.
- `/verifyall` now reports S57.2 build identity and evaluates the actual S57.2 route bindings.
- `/buildinfo` and `/routeraudit` now require all identity-critical routes to match their S57.2 handlers.
- Registry remains frozen at 341/341; compatibility commands remain virtual and consume no registry slots.
- Final Telegram application callback is rebound after S57.2 routes are installed.

## Preserved
- Schema 1
- Paper 20
- Shadow 60
- Live Trading OFF
- Synthetic completion OFF
- Release Gate formulas and evidence values unchanged
- Existing runtime data, snapshots, learning data, and settings preserved
