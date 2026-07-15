# A100 V116.0 LTS Permanent Baseline Contract

## Official baseline
- Version: A100 V116.0-LTS-S2.18.2
- Parent baseline: S2.18.1
- Recovery reference: S2.17.29
- Release mode: Feature Freeze / Release Freeze

## Non-negotiable invariants
- Telegram commands: 341
- Schema: 1
- Paper positions: 20
- Shadow positions: 60
- Live trading: OFF
- Existing data and environment configuration must remain untouched.
- READY, COLLECTING and IN PROGRESS never count as PASS.
- Scores must come from authoritative persisted evidence only.

## Protected implementation
- Single immutable runtime state per Snapshot ID + Unified Hash.
- Single evidence source.
- Single active version source.
- Unified formatter for status/runtime/release/LTS views.
- One gate calculation per authoritative snapshot.
- Read-only command fast paths with no storage scan or evidence rebuild.
- Startup prewarm and cache reuse.
- RuntimeHealth and ReleaseGate command isolation.
- 341-command registry/callable/help/route linkage.

## Formula freeze
S2.18.2 does not change the S2.18.1 gate matrix, thresholds or fast-context score inputs.
A formula fingerprint regression test blocks accidental edits to those paths.

## Release rule
A later release must fail its build if any protected invariant, command linkage,
formula fingerprint or executable-entrypoint rule regresses.
