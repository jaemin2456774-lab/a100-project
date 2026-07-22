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
