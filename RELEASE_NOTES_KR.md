# A100 V118.0 RC3.3 릴리즈 노트

Build ID: V118.0-RC3.3-20260722-RECOVERY-PROFILING-SNAPSHOT-RENDER-CACHE-FASTPATH-01

## 수정 범위
- Recovery 단계를 recovery_core / projection_warmup / trust_warmup으로 세분화
- Projection Snapshot TTL 30초 추가
- Trust Snapshot을 Projection Hash 기준으로 재사용
- Render Cache 저장 시각을 build 완료 시점으로 수정
- /commandcert, /commandmatrix, /trustgate, /intelligencescore Snapshot Fast Path 적용
- /intelligencescore 레거시 end-to-end 호출 제거 및 Strict Read Only 렌더 경로 적용
- /performance에 Hits / Misses 명시
- Registry 341/341, Live Trading OFF, Ledger Append Only 유지
