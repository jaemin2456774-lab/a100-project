# A100 V96.2 AI Intelligence 3

Development release based on V96.1 AI Intelligence 2. Upload the contents of this folder to the repository root.

## New commands
- `/aicalibration` — Confidence predicted vs actual calibration
- `/aimemorybank` — 1D / 7D / 30D / ALL memory windows
- `/airank BTC ETH SOL` — multi-candidate ranking
- `/shadowreplay` — Shadow learning outcome replay
- `/aihealth` — unified AI health monitor

## Preserved
- schema 1 and `a100_v91_paper_state.json`
- paper maximum 20 and shadow maximum 60
- all V96.1 and earlier commands
- no live-order path

## Validation
Focused V96 regression suite: 9 passed. See `docs/TEST_REPORT_V96_2.md`.
