# CHAT HANDOFF — CURRENT

## Baseline
V118.0-RC3.13.17
Build: V118.0-RC3.13.17-20260724-RUNTIME-SYMBOL-RECOVERY-ULTIMATE-FANOUT-RETIREMENT-01

## Root cause
RC3.13.16 function replacement consumed the module-level runtime declaration block.
This removed the isolated-render thread local and filtered/refinement locks.

## Fix
- Rebuilt from verified RC3.13.15 source.
- Runtime globals preserved and audited 8/8.
- Ultimate direct/default/detail use fast Runtime Read View only.
- Ultimate removed from automatic reader fanout.
- Heavy dispatcher blocks Ultimate.
- Sniper/Paper/Shadow retained.
