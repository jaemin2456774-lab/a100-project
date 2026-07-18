# A100 V116.1 DEV S57.3 Changelog

## Title
Authoritative Virtual Route & Output Identity Recovery Hotfix

## Fixed
- `/version` and `/runtimehealth` legacy LTS handlers winning after startup restore/reconcile.
- `/status` and `/runtimehealth` old LTS headers escaping through non-`reply_text` output paths.
- `/verifyall` retaining S57/S57.2 build identity and stale route summaries.
- Registry physical replacement being overwritten after initialization.

## Implementation
- Expanded authoritative virtual routes to seven commands: version, status, runtimehealth, buildinfo, connectivity, verifyall, routeraudit.
- Final dispatcher resolves authoritative virtual routes before physical Registry entries.
- Added identity normalization for message reply, bot send, and message edit paths.
- Preserved existing LTS metrics, release-gate values, 72-hour evidence, data, and settings.
- Registry remains 341/341; no new physical command slots.

## Safety invariants
Schema 1 · Paper 20 · Shadow 60 · Live OFF · Synthetic completion OFF · Gate unchanged.
