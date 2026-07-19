# A100 V116.1 DEV S59.7.12

## Adaptive History & Champion Evolution Long-Runtime Validation

- Added bounded hourly Adaptive History (max 168 points).
- Repeated command calls within the same hour update one point instead of creating synthetic history.
- Added LONG/SHORT candidate trend and Shadow agreement trend.
- Added Feature Ranking history and rank-churn evidence.
- Added Champion generation fingerprint history.
- Champion repeated evidence counts only distinct hourly qualified observations: samples >=100 and EV >0.
- Promotion remains recommendation only.
- No Paper/Live/Gate weight mutation.
- Registry 341/341 and existing runtime/learning data preserved.
