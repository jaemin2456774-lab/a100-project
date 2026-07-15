# A100 V116.0 LTS S2.17.25

## Fixed
- Unified legacy RC4/S2 version tokens at the final reply boundary so active outputs identify S2.17.25.
- Replaced legacy Strategy Trust presentation with an authoritative persisted-outcome evidence view.
- Added Gate 1–5 PASS/BLOCKED state, score gap, and evidence blocker reasons.
- Added Outcome Quality coverage and evidence blocker diagnostics.
- Pinned runtime score composition to snapshot identity; repeated reads of the same snapshot return the same score.

## Preserved
- Telegram commands: 341
- Schema: 1
- Paper: 20
- Shadow: 60
- Live trading: OFF
- Feature Freeze / Release Freeze: ACTIVE
- Existing data and configuration are not modified.
