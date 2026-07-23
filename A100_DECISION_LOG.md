# DECISION LOG

## Locked decisions
- Important meetings, ideas, reasons, roadmap, lessons, and chat handoff are stored as repository files with every patch.
- ChatGPT memory is supplementary; repository project memory is the durable handoff source.
- Moving to a new chat requires updating and carrying `CHAT_HANDOFF.md`.
- Mid-sprint user observations are incorporated naturally as hotfixes, optimizations, or Future Queue items.
- They do not automatically rewrite the large roadmap.
- Repeated promises are not a substitute for code, tests, and updated project-memory files.
- System stabilization must not be delayed by unplanned feature expansion.


## Mobile-first packaging lock
- A100 release packages are MOBILE FLAT by default.
- `UPLOAD_FILES` must contain root files only unless the user explicitly requests folders.
- The user must not be required to create directories from a phone.
- Project-memory files are shipped as flat root files and committed with the source.


## RC3.11.3.1 boot hotfix
- Import-time symbol references must never be assigned before the referenced function exists.
- Warmup wrappers must not self-reference or recursively capture themselves.
- Boot-critical patches require compile validation and import-order inspection.


## RC3.11.3.2 boot-definition recovery
- Marker-based replacement must not span unrelated boot classes.
- Every instantiated class must be statically verified as defined earlier in the module.
- Boot-critical symbol integrity is checked before packaging.


## RC3.11.3.3 performance symbol compatibility
- New handlers must be validated against all referenced global names, not only Python syntax.
- Static compile does not detect runtime global-name resolution failures.
- Release validation must include symbol existence and handler smoke execution.


## RC3.11.3.4 live diagnostic rule
- Commands that report cache/warmup/metric state must not cache their own output.
- `/performance` is a live diagnostic and always bypasses Shared Cache.
- Stable command outputs may be boot-warmed; live state dashboards must render current state.


## RC3.11.3.5 sender contract hotfix
- Direct Telegram sender calls use:
  `_v1180_send_direct(update, text, command)`.
- Packaging validation uses Python AST to verify every call site.


## RC3.11.4 heavy-command isolation
- Heavy read-only commands must not execute inside Telegram's dispatcher timeout.
- `/paper`, `/sniper`, and `/shadow` use background authoritative rendering plus
  bounded snapshots.
- First request may report preparation; subsequent requests use FAST PATH.
- Stale-while-refresh is allowed for monitoring output and is labeled clearly.
- No synthetic trading/certification evidence is created.


## RC3.11.5 heavy snapshot persistence
- Heavy output snapshots persist on Railway volume.
- Heavy refresh concurrency is one.
- User requests receive refresh priority.
- Persisted output is read-only cache, never certification evidence.


## RC3.11.6
- Warm Path is cache readiness SSOT.
- Snapshot older than 3×TTL is EXPIRED and not displayed.
- Scheduler status must show running/waiting/queue.


## RC3.12.0 real runtime factor bridge
- Producer output and consensus input names are a versioned contract.
- Structured real observations may be exposed through numeric compatibility
  fields with explicit provenance.
- Missing News remains missing unless a real numeric observation exists.
- Synthetic zero-fill and fabricated coverage are prohibited.


## RC3.12.1 stability decisions
- Heavy render work uses a bounded lease token.
- Expired or detached workers can never commit stale results.
- Snapshot commit is atomic and generation-monotonic.
- Invalid/delisted symbols are quarantined; transient API failures are retried.
- PRICE_UNAVAILABLE is an external data condition, not a strategy failure.
- Latest deployed ZIP is the mandatory development SSOT.


## RC3.12.2 heavy stage budget decisions
- A queued command is WAITING, never EMPTY.
- Heavy state is WAITING → BUILDING_RENDER → COMMITTING → READY.
- Lease budgets are command-specific and based on observed runtime cost.
- Automatic retry is bounded; endless requeue loops are prohibited.
- Cold boot eagerly computes only Sniper to reduce contention.
- Paper and Shadow are lazy heavy snapshots.

## RC3.12.3
- Measure only real pipeline stages.
- READY requires post-commit verification.
- Failed verification must not report READY.
- Latest deployed ZIP remains development SSOT.


## RC3.12.4
- Renderer sub-stage labels must be derived from the actually executing stack.
- Stack sampling is diagnostic only and cannot mutate engine decisions.
- Active function, line, sample count, and unchanged duration identify the real
  bottleneck before optimization.
