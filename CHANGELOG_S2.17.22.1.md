# A100 V116.0-LTS-S2.17.22.1

## Release Gate Path Type Safety Hotfix

- Fixed `TypeError: stat: path should be string, bytes, os.PathLike or integer, not dict` in the non-blocking `/releasegate` background job.
- Added a centralized path normalizer for legacy path strings, `PathLike` values, and snapshot metadata dictionaries.
- Supported metadata keys: `path`, `filepath`, `file_path`, `filename`, `file`, `location`, and `content_location`, including one nested metadata level.
- Invalid or missing path metadata is skipped safely instead of aborting Release Gate diagnostics.
- Applied the same defensive normalization to merged runtime-history and evidence-file readers.
- Preserved Schema 1, Paper 20, Shadow 60, Live OFF, `/data`, Registry 341, and all authoritative gate thresholds.
