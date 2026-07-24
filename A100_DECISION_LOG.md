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


## RC3.12.5
- Repeated V91 state reads use file-signature cache rather than repeated JSON parsing.
- Save refreshes the cache atomically after the state file replacement.
- Cached state is returned as a defensive copy.
- Telegram HTML parse failure must fall back to plain text instead of failing the command.


## RC3.12.6
- Heavy Snapshot generation is a read-only projection of existing Runtime data.
- Private Snapshot event loops must never initiate exchange/network scans.
- Stale real Runtime cache may be displayed with explicit age; missing cache
  remains empty and cannot be synthetically completed.
- Normal runtime scan authority remains unchanged.


## RC3.12.7
- Heavy Scheduler wake is event-driven.
- Every queue push immediately sets the wake event.
- Lease ownership starts after worker assignment.
- READY follows COMMIT and VERIFY only.


## RC3.12.8
- A boolean worker-started flag is insufficient; thread liveness is authoritative.
- Worker entry exceptions must never terminate the scheduler silently.
- Queue pop and worker entry are explicit guarded transitions.
- New queue requests reset stale display telemetry.


## RC3.12.8.1
- Stack classifier local variables must be initialized before any branch uses them.
- This release is a minimal runtime hotfix; no architecture or roadmap changes.


## RC3.12.9
- Runtime Scan Cache requires an explicit producer; Snapshot must remain a consumer.
- Every producer commit is generation-monotonic and verified.
- Empty scan, empty filter, empty cache, and failed commit are distinct states.
- Heavy warmup should not race ahead of the first producer cycle.

## RC3.13.0
- Producer stages must be bounded.
- Unproduced or unverified empty Sniper output cannot be published FRESH.
- Read-only projections use bounded structural read views.
- Stabilization scope only; roadmap unchanged.


## RC3.13.1
- Heavy worker must not block on JSON serialization or fsync.
- In-memory atomic swap is the query authority; persistence is background recovery evidence.
- Persistence requests are coalesced through one worker.
- Timeout-produced empty data is not equivalent to a successful empty scan.


## RC3.13.2
- Snapshot render cannot wait for Runtime Producer.
- Producer completion hands verified generation to Snapshot queue.
- Incomplete producer state returns WAITING_FOR_RUNTIME_PRODUCER without render.
- Last verified Snapshot remains the read-only fallback.


## RC3.13.3
- Filtered timeout must terminate in a safe committed state, not indefinite WAIT.
- Existing verified cache is preferred over overwriting with timeout-empty data.
- First-boot timeout may publish only explicit DEGRADED_EMPTY / WAIT evidence.
- Raw fallback runs independently and single-flight, then upgrades the cache.

## RC3.13.4
- Isolated query rendering may not mutate V91 state.
- Render, commit, persistence queue, verification and READY are separate observable transitions.


## RC3.13.5
- Producer generation is the Reader Attach identity.
- The same generation may be rendered once per reader, not repeatedly queued.
- Sniper completion fans out Paper and Shadow with fair queue priority.
- Reader state transitions are observable and persistent in telemetry.

## RC3.13.6
- Filtering is published once per Producer generation.
- All Heavy readers share one immutable View identity.
- Unknown coverage loss is reported as UNCLASSIFIED, never invented.
- Raw Recovery remains background-only.


## RC3.13.7
- /ultimate is a Heavy read-only view and must never run under the 12-second legacy dispatcher.
- Coverage Audit must satisfy Classified + Unclassified = Dropped.
- Reader lag is shown explicitly as Pending generation delta.


## RC3.13.8
- Slow filtered analysis is a background refinement, never a first-response dependency.
- A verified non-empty last-good View has precedence over degraded/timeout empty data.
- First boot uses bounded Raw-first evidence; analysis readers wait rather than certify empty.
- Reader output must disclose LAST_GOOD/CURRENT and pending refinement state.


## RC3.13.9
- Reader attachment is idempotent for a Producer generation.
- Direct user requests may promote queued work; background fanout may not starve them.
- Ultimate is on-demand, not Producer-eager.
- A usable last-good snapshot is served immediately while replacement renders.
- ATTACH_OK requires a real Shared View ID.


## RC3.13.10
- Telegram output must be paginated before transport.
- Default /ultimate is compact; detail is explicit.
- Identical Producer generation/content maps to one stable View ID.
- Empty evidence is cacheable and must not cause View churn.
- Every dropped row is visible as a classified bucket or Unclassified.

## RC3.13.11
- Startup task handles require explicit global scope.
- All legacy run_bot_async variants must be audited.
- Direct handler symbols must exist before final application construction.


## RC3.13.12
- Final direct-route registration requires complete symbol closure.
- Startup audits all direct handlers together before application construction.
- Missing route symbols must fail once with a complete list, never serially
  across repeated deployments.


## RC3.13.13
- Default /ultimate is a compact runtime-cache reader, not a Heavy renderer.
- Heavy Ultimate is explicit through /ultimate detail only.
- /start and /help must use the current product contract, never legacy banners.
- /commands is derived from the authoritative registry.

## RC3.13.14
- Compact renderers must tolerate runtime schema variation.
- Unknown candidate schemas must render safe key hints, never blank output.


## RC3.13.15
- Runtime candidates may be dictionaries, dataclasses, or ordinary objects.
- Compact renderers use a shared safe attribute adapter.
- Result.sym/action/confidence/score/prob24 are authoritative fallback fields.
- Old errors remain evidence and are visually distinguished from new failures.


## RC3.13.17
- Function replacement boundaries must stop before module globals.
- Runtime global symbol audit is mandatory before release.
- Ultimate is excluded from automatic heavy reader fanout.
