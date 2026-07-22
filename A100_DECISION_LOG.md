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
