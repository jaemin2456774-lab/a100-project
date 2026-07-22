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


## V118.0 RC3.10
- Command DNA v2 mirrors measured Certification SSOT into the inventory projection.
- No synthetic PASS, no ledger append, no command execution at boot.
- Core Phase-1 commands are tagged and reported separately.
- Mobile-First incremental patch remains mandatory.


## RC3.10.1 Trust Cache Coherency Hotfix
- Boot warmup before live-worker freshness could cache Runtime Integrity 0.
- Trust snapshots and trust render cache are now keyed by authoritative runtime freshness generation (`rf0`/`rf1`).
- Version Audit and Platform Trust must remain internally consistent after worker freshness becomes PASS.


## V118.0 RC3.10.2 Telegram Startup Recovery
- Healthcheck PASS and Telegram BOT READY are separate states.
- Process-lock contention must never leave a silent infinite-sleep container.
- Lock acquisition uses bounded retry and then fails the process for Railway restart.
- Telegram lifecycle logs must remain visible.
- `/tmp/a100_telegram_ready.json` records LOCK_WAIT, LOCK_ACQUIRED, INITIALIZING,
  FAILED, CANCELLED, or timeout state without touching `/data` or trading state.


## V118.0 RC3.10.3 Telegram Update/Dispatch Recovery
- Polling-started logs alone are not treated as proof of command operation.
- Telegram RECEIVE, direct SEND, and legacy dispatcher are measured separately.
- `/version` and registry-neutral `/ping` probes run before the legacy dispatcher.
- Direct probes do not add entries to the authoritative 341 command registry.
- Every received command logs update_id/chat_id and dispatcher entry/completion/failure.


## V118.0 RC3.10.4 Dispatcher Deadlock Recovery
- One blocked command must never hold the sequential Telegram update queue indefinitely.
- The legacy dispatcher has a bounded 12-second outer timeout and releases the queue.
- `/help`, `/start`, `/commands`, `/version`, and registry-neutral `/ping` use direct handlers.
- Direct sends have a bounded timeout with sent/failed/timeout evidence.
- Registry, Certification, Ledger, Learning, and Trading Gate remain unchanged.


## V118.0 RC3.10.5 Concurrent Core Thread Fast Path
- Slow core monitoring commands run in isolated worker threads with private event loops.
- Fake Telegram replies capture rendered output, preventing late duplicate responses after timeout.
- Up to four core commands can execute concurrently.
- Telegram's main asyncio loop stays responsive while file, ledger, projection, or cache work runs.
- Registry, Certification, Ledger, Learning, and Trading Gate remain unchanged.
