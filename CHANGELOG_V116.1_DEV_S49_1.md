# A100 V116.1 DEV S49.1

## Explainable AI Brain Schema Compatibility & Startup Audit Isolation Hotfix

- Fixed Railway boot crash: `TypeError: float() argument must be a string or a real number, not 'dict'`.
- Added bounded read-only numeric extraction for both legacy numeric and current structured `long_brain`, `short_brain`, and `wait_brain` payloads.
- Supported structured keys: `score`, `brain_score`, `value`, `probability`, `confidence`, `strength`, and `weighted_score`.
- Added one-level nested compatibility for `result`, `metrics`, `summary`, and `decision` payloads.
- Isolated non-critical Explainable AI static-audit exceptions so diagnostic failure cannot create a Railway restart loop.
- Critical startup checks remain enforced: Registry 341/341 and active command routes.
- Runtime First, Strict Read Only, Evidence Only, Schema 1, Paper 20, Shadow 60, Live OFF, and existing data are preserved.
