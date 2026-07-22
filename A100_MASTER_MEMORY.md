# A100 MASTER MEMORY

## Authoritative baseline
- Current development baseline: A100 V118.0-RC3.8.
- This patch advances identity to V118.0-RC3.9.
- Architectural recovery baseline remains V116.0 LTS S2.17.26.
- Railway is the only deployment environment. Render terminology is obsolete.

## Immutable platform principles
1. Runtime First: live runtime is the execution SSOT.
2. Snapshot is evidence/recovery only; it must not replace live runtime truth.
3. Telegram commands are strict read-only monitoring paths.
4. Ledger is append-only and hash-chain protected.
5. Certification PASS requires measured evidence; synthetic completion is prohibited.
6. Existing data, learning state and configuration must be preserved.
7. Schema 1, Paper 20, Shadow 60 and Live Trading OFF remain fixed until separately approved.
8. Registry integrity target is 341/341.
9. Regression prevention and runtime stability precede new features.
10. Routine releases use incremental patches; full packages are reserved for major milestones.

## Product and AI direction
- Preserve separate Long AI, Short AI and WAIT evaluation.
- Final decisions are consensus-based, not single-signal decisions.
- Evidence sources include chart, news, funding, open interest, volume, whale activity, regime and learning evidence.
- Preserve Explainable AI, self-review, outcome attribution, strategy trust, champion lifecycle and adaptive learning.
- Promotion path remains Shadow -> Paper -> Canary -> Live.

## Command certification program
- Final target: PASS 341 / PARTIAL 0 / FAILED 0.
- Registration alone is insufficient.
- Every command must be checked for runtime, handler, engine, evidence, output, storage, replay, performance, documentation and regression.
- Command DNA is the stable identity card for each command.
- Runtime registry export is read-only and may create replaceable projection files only.

## Engineering continuity
- Engineering Library is the Design SSOT.
- Important decisions belong in MASTER_MEMORY, HANDOFF, ADR, Decision Log or Promise Ledger.
- Before a new version, prior meeting decisions must be reviewed and reconciled.
- New ideas do not overwrite the frozen roadmap; they enter an Icebox until approved.
- Sprint reports use Completed / In Progress / Next / Risks.

## Mobile-first delivery
- The user primarily works from a phone.
- Mobile GitHub and Railway workflows are the default.
- Patches must minimize folder creation, path entry and multi-step uploads.
- Root-level changed files are preferred when technically safe.
- Every patch includes installation steps, QA commands, rollback guidance and SHA256.

## Roadmap order
1. Engineering memory and foundation.
2. Runtime foundation stability.
3. Authoritative 341-command inventory and Command DNA.
4. End-to-end command certification.
5. Long/Short/WAIT intelligence integration.
6. Learning and Trust integration.
7. Mission Control and dashboards after authoritative sources are ready.
8. FC -> LTS -> Stable -> TrustOS.

## Lessons that must not be repeated
- Do not call a document-only package a runtime feature release.
- Do not claim PASS from registration or placeholders.
- Do not introduce a new command merely to observe existing state if registry neutrality is required.
- Do not make mobile users manually recreate complex directory trees.
- Do not change gate calculations while performing observability or documentation work.
- Do not silently lose previously agreed roadmap items when moving chats.
