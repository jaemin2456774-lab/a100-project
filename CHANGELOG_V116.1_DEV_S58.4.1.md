# A100 V116.1 DEV S58.4.1 Changelog

- Replaced the undefined ledger writer with a self-contained atomic JSON writer.
- Added unique temporary files, flush, fsync, and os.replace for ledger safety.
- Installed current S58.4.1 handlers for status, runtime health, build info,
  connectivity, router audit, version audit, engine audit and certification commands.
- Unified current route expectations to remove S57.8/S58.4 identity conflicts.
- Preserved Runtime Ledger, Engine E2E, command certification and all trading invariants.
