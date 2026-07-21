# A100 V117.0 RC3 릴리스 노트

Build ID: `V117.0-RC3-20260721-REGISTRY-RECOVERY-READONLY-TRUST-ATOMIC-BACKUP-01`

## 수정 내용

- 인증된 historical exact-341 command baseline으로 Registry membership 복원
- V117 RC2에서 현재 343개 Registry를 새 expected set으로 고정하던 회귀 제거
- `/trustgate`, `/intelligencescore`를 완전 read-only Projection 조회로 변경
- Trust 조회 시 trust snapshot 및 immutable ledger event append 금지
- V75 volume backup 저장에 전용 lock, 고유 same-directory temp file, fsync, atomic replace 적용
- 원자적 백업 실패 시 한 차례 bounded retry 후 warning/error ledger 기록
- RC2의 single startup path와 lazy SSOT 성능 최적화 유지

## 변경하지 않은 항목

- Registry command 추가 없음
- Historical 데이터 삭제 및 rewrite 없음
- Entry Gate, Threshold, Learning, Attribution, Paper, Shadow, Live 경로 변경 없음
- Live Trading OFF 유지
