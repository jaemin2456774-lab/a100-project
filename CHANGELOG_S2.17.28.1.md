# A100 V116.0 LTS S2.17.28.1

## Emergency startup preflight hotfix

- Fixed Railway restart loop caused by certification-only preflight findings being treated as fatal startup blockers.
- Split preflight result into `startup_ok` and full certification `ok`.
- Only operational integrity failures can stop startup.
- Version-source and output-root certification findings remain visible in startup logs and `/versionaudit` without terminating the bot.
- Added explicit failed-item logging before any operational abort.
- Preserved 341 commands, Schema 1, Paper 20, Shadow 60, Live OFF, data and settings.
