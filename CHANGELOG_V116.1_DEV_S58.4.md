# A100 V116.1 DEV S58.4 Changelog

- Updated `/engineaudit` title and Build ID to the current S58.4 metadata.
- Added a persistent read-only Telegram command runtime invocation ledger.
- Records handler completion, response output count, failures and timestamps.
- PARTIAL commands are promoted to PASS only after successful live invocation
  and at least one observed output.
- Added `RUNTIME_CERT` visibility to `/commandmatrix`.
- Updated `/commandcert`, `/regressionguard`, `/verifyall` to S58.4 identity.
- Existing engine, gate, learning and trading logic remains unchanged.
