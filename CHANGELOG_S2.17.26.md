# A100 V116.0 LTS S2.17.26

## Shared Snapshot Fast Path Certification

- `/status` synchronous full certification rebuild removed.
- `/pipelinetrace` changed to read-only shared snapshot output.
- `/ltscertification` changed to shared snapshot gate summary.
- Cold/warming state returns immediately instead of blocking Telegram requests.
- Background workers remain responsible for refresh and persisted evidence collection.
- Snapshot-pinned Runtime score and authoritative gate semantics preserved.
- Version source unified to S2.17.26.
- Registry remains 341 commands; Schema 1, Paper 20, Shadow 60, Live OFF preserved.
