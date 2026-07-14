# A100 V116.0 LTS-FC1 Change Ledger

| ID | 변경 목적 | 수정 영역 | 영향 범위 | 검증 | 회귀 결과 | 상태 |
|---|---|---|---|---|---|---|
| FC1-001 | 과거 릴리스 증거 훼손 방지 | `main.py` VersionManager/역사 상수 | `/version`, `/status`, preflight, 모든 버전 감사 | Version snapshot 테스트 | 83/83 PASS | CERTIFIED |
| FC1-002 | 현재 버전 단일 출처 확립 | `main.py` | Runtime version, release gate | `V91_VERSION == V1160_VERSION_MANAGER.version` | PASS | CERTIFIED |
| FC1-003 | 누적 테스트의 오래된 현재값 가정 제거 | 회귀 테스트 | RC4.9.21~25 및 LTS-FC1 | 전체 pytest | 83/83 PASS | CERTIFIED |
| FC1-004 | LTS-FC1 인증 증거 추가 | 신규 FC1 테스트/보고서 | Schema, Paper, Shadow, Live, Freeze | Preflight + pytest | PASS | CERTIFIED |
