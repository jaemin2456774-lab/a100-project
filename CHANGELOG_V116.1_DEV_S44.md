# A100 V116.1 DEV S44 Changelog

## Memory Leak Containment & Certification Continuity Hotfix

- Added 60-second bounded memory pressure guard.
- Added configurable soft/hard thresholds (`A100_S44_MEMORY_SOFT_MB`, `A100_S44_MEMORY_HARD_MB`).
- Added bounded cleanup for expired S37 evidence/render caches.
- Added bounded trimming for S41 resource samples.
- Added GC request after containment actions.
- Added persistent boot continuity marker under `/data/v1161_s44_boot_continuity.json`.
- Added `/version` and `/god` memory pressure/continuity evidence.
- Preserved S43 certification diagnostics and all S27-S43 cumulative features.
- No Runtime, Final AI, Telegram, certification evidence, release gate, consensus, order, or adaptive-weight mutation.
