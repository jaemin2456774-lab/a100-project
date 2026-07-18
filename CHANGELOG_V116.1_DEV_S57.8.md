# A100 V116.1 DEV S57.8 Changelog

## Final Metadata Single Source Consistency Polish

- Replaced the `/version` proxy chain with an independent S57.8 renderer.
- Removed stale S57.5 title metadata.
- Removed stale `Identity Audit FAILED` output derived from an older audit.
- Version, title, Build ID, identity result, route count, and Registry count now come from the current S57.8 audit.
- Normalized status, runtime health, connectivity, engine audit, version audit, and verify-all metadata to S57.8.
- Preserved Engine E2E logic and all S57.7 runtime evidence.
- Major UI redesign remains deferred until functional development is complete.
- Registry remains 341/341; Live Trading remains OFF.
