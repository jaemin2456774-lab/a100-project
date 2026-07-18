# A100 V116.1 DEV S56.1

## Deployment Build Integrity Hotfix
- Added `/buildinfo` dispatcher route without increasing Registry 341.
- `/version` now exposes immutable Build ID `S56.1-20260718-BUILD-INTEGRITY-01`.
- Startup preflight now verifies active version/verifyall handlers, connectivity route, buildinfo route, and Registry 341/341.
- Startup logs print exact version and Build ID so Railway deployment can be verified without screenshots.
- Preserved S56 producer connectivity bridge, `/connectivity`, `/verifyall`, Runtime First, Strict Read Only, Gate unchanged, Schema 1, Paper 20, Shadow 60, Live OFF.
