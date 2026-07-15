# A100 V116.0 LTS S2.17.29.1
## Live State Builder Recursion Hotfix

- Fixed infinite recursion in `_v1160_s21729_build_live_state`.
- Frozen the original S2.17.28 live-state builder under a private base alias before compatibility rebinding.
- Preserved Live Runtime Worker, strict Telegram read-only path, 30-second evidence change detection, and 341 commands.
- Added regression coverage that rejects direct self-referential builder calls.
- No schema, data, Paper/Shadow, gate threshold, or trading-mode changes.
