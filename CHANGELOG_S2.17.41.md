# A100 V116.0 LTS S2.17.41

## Startup Preflight Order Fix & Release Candidate Stabilization

- Fixed Railway restart loop introduced in S2.17.40.
- Root cause: inherited S2.17.39 preflight restored older route handlers after S2.17.40 reconciliation, so the final S2.17.40 checks falsely reported the current handlers as inactive.
- Current release handlers are now reconciled both before and after the inherited preflight.
- Startup still fails closed for genuine unrecoverable structural faults only.
- Registry 341, Runtime First, Strict Read Only, Evidence Worker, Schema 1, Paper 20, Shadow 60 and Live OFF preserved.
- Release Gate formulas and thresholds unchanged.
