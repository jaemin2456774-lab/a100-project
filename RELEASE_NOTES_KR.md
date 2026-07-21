# A100 V117.0 RC1 Release Notes

## 빌드
- Version: `V117.0-RC1`
- Build ID: `V117.0-RC1-20260721-CERTIFICATION-SSOT-IMMUTABLE-LEDGER-TRUST-ENGINE-01`

## 핵심 변경
- Certification SSOT 도입: Command Certification, Command Matrix, Version Audit, Trust가 동일 Projection을 읽습니다.
- 단일 Rule Engine `v117.ssot.rule.v1` 도입.
- Command State Machine: DISCOVERED → REGISTERED → OUTPUT_VERIFIED → RUNTIME_VERIFIED → EVIDENCE_VERIFIED → STORE_VERIFIED → CERTIFIED.
- Append-only JSONL Certification Event Ledger와 SHA-256 hash chain 도입.
- Trust Engine v1 도입. Runtime, Ledger, Replay, Historical, Certification Coverage를 동일 가중치로 계산합니다.
- 기존 `/trustgate`를 Platform Trust Report로, `/intelligencescore`를 Trust Score 요약으로 승격했습니다.
- Registry 341/341 고정을 위해 신규 Telegram 명령은 추가하지 않았습니다.

## 변경하지 않은 영역
- Entry Gate / Threshold
- Learning / Attribution 생산 경로
- Paper / Shadow / Live 주문 경로
- Historical anomaly 데이터
- Replay 원본 데이터
- Live Trading OFF
