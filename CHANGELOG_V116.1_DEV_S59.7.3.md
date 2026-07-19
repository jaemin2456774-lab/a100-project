# A100 V116.1 DEV S59.7.3 Changelog

## Scope
Current Audit Route / Replay Hash Baseline / Drift Key Alignment Hotfix.

## Fixed
- Replaced legacy S59.7 version audit passthrough with a current S59.7.3 authoritative route audit.
- Version audit now checks the handlers currently installed in the virtual router and reports mismatches directly.
- Rebuilt Evidence Replay using one canonical original/roundtrip hash domain.
- Missing replay source is reported as MEASURING rather than fabricated PASS/FAILED.
- Corrected Cross-Engine Drift key mapping to the actual S59.1 report fields:
  snapshot_id_single, runtime_root_single, revision_integrity, engine_e2e, producer_16_16.
- Propagated corrected Replay/Drift functions into downstream Matrix and RC calculations.
- No new Telegram command and no Registry cardinality change.

## Preserved
Runtime First, Strict Read Only, Registry 341, Schema 1, Paper 20, Shadow 60, Live OFF, Synthetic Completion OFF, Gate Formula unchanged, existing Runtime/Learning data.
