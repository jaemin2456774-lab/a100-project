# A100 V116.0 LTS-S2.1 Long Runtime Certification

## 개발 목적
Sprint 1 인증 기준선을 변경하지 않고 24~72시간 장시간 안정성 인증에 필요한 운영 계측을 추가한다.

## 반영 사항
- 72시간 인증 진행률과 연속 세션 가동시간
- 별도 런타임 인증 상태 파일(`data/lts_sprint2_runtime.json`)
- Memory/CPU/Thread/Queue/Cache 표본 수집
- 1h/6h/24h 메모리 추세
- P95 및 자원 Drift 표시
- Process Restart, Auto Recovery, Snapshot Restore, Exception Recovery 카운터
- Runtime Evidence와 Long Runtime Dashboard
- 기존 341개 명령, Schema 1, Paper 20, Shadow 60, Live OFF 유지

## 자동 인증 결과
- Pytest: 83/83 PASS
- Registry/Handler/Help/Output: 341/341
- Version Source: Single
- Release Freeze: ACTIVE
- Regression Risk: NONE
- Sprint 2 상태: MEASURING

## 주의
이 릴리스는 장시간 인증을 시작하기 위한 계측 릴리스다. 실제 24~72시간 운영 결과가 축적되기 전에는 Sprint 2를 CERTIFIED로 선언하지 않는다.
