# 설치 및 QA

1. Railway 프로젝트의 기존 `main.py`를 패치의 `main.py`로 교체합니다.
2. 기존 `/data` 볼륨을 유지한 채 재배포합니다.
3. 다음 순서로 실행합니다.

```text
/version
/buildinfo
/versionaudit
/commandcert
/commandmatrix
/trustgate
/intelligencescore
/commandcert batch 1 run
/commandcert status
/versionaudit
/trustgate
/errors
```

## 정상 기대값
- Version / Build: V117.0-RC1 정렬
- Registry: 341/341
- Certification SSOT: PASS
- Immutable Ledger Hash Chain: PASS
- Command Certification과 Command Matrix의 PASS/PARTIAL/FAILED 수 일치
- `/trustgate`: Runtime/Ledger/Replay/Historical/Coverage 및 정직한 Overall Trust 표시
- Runner 기존 모드 정상 동작
- Historical QA/Unknown growth 0 유지
- Live Trading OFF

## 생성되는 운영 파일
- `/data/a100_v117_certification_events.jsonl`
- `/data/a100_v117_certification_projection.json`
- `/data/a100_v117_trust_snapshots.json`
