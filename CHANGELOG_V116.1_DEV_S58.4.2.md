# A100 V116.1 DEV S58.4.2 Changelog

- Replaced the nonexistent Ledger JSON reader with a local safe reader.
- Added Ledger root-type validation.
- Corrupt Ledger files are moved to a timestamped backup before recovery.
- Ledger writes now perform immediate read-back and value comparison.
- Added startup round-trip self-test.
- Added Ledger read/write/round-trip status and entry count to audits.
- Updated Command Certification, Runtime Matrix, VerifyAll and Engine Audit titles to S58.4.2.
- Engine, gate, learning and trading logic remain unchanged.
