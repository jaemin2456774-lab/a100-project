# A100 V116.0 LTS S2.17.28

## Fixed
- Removed the nested output-wrapper reversal that changed the active S2.17.27 token back to S2.17.25.
- Final Telegram output now bypasses the legacy S2.17.25 compatibility wrapper and performs one normalization pass only.
- Replaced the legacy S2.17.25 `/versionaudit` handler with an S2.17.28 active handler.
- Version Source Single now validates V91_VERSION and VersionManager number/version against the same active source.
- `/version`, `/runtimehealth`, `/releasegate`, and `/versionaudit` are registered to active S2.17.28 handlers.

## Preserved
- 341 Telegram commands
- Schema 1
- Paper 20 / Shadow 60
- Live Trading OFF
- Existing `/data`, environment variables, and configuration
- Feature Freeze / Release Freeze
