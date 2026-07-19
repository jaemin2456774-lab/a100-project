# A100 V116.1 DEV S59.7.2

## Ledger Format Compatibility · Runtime Evidence Recovery · Identity Route Truth

- Fixed generic JSON reader that incorrectly required every JSON root to be a dict.
- Added backward-compatible list-root command ledger conversion.
- Preserved list-root certification history files.
- Removed repeated valid-history `.corrupt` rotation behavior.
- Rebuilt Ledger → Evidence → Replay → Matrix cache after compatibility recovery.
- Restored authoritative current-route identity verification for S59.7 handlers.
- Preserved Runtime First, Strict Read Only, Registry 341, Schema 1, Paper 20, Shadow 60, Live OFF and Synthetic Completion OFF.
- No Gate Formula change and no destructive Runtime/Learning data reset.
