# A100 V116.0 RC4.9.15 개발 릴리즈 보고서

## 목적
RC4.9.14 실배포 캡처에서 확인된 Version Audit 불일치, Command Certification 오해 가능성, Repository/Runtime 0 표시, 캐시 최신성 불명확, Batch backlog와 대화형 지연 혼합 문제를 수정했습니다.

## 핵심 수정
- `/version`, `/versionaudit`를 RC4.9.15 활성 VersionManager에 연결했습니다.
- Registry 구조 검증과 실제 Runtime Probe 증거를 분리했습니다.
- `Registry Verified 341/341`과 `Runtime Probed / E2E Pending`을 별도로 표시해 15개만 검증된 것처럼 보이던 문제를 수정했습니다.
- Repository, Output, Runtime은 0개 그룹이라는 모호한 표현 대신 실제 probe evidence 수를 표시합니다.
- `/commandcert deep`에서만 비용이 큰 Read-Only Runtime Probe를 새로 수행하도록 하여 기본 응답 지연을 줄였습니다.
- Cache HIT에 Age와 Remaining TTL을 표시합니다.
- Performance Audit에서 누적 Batch Backlog를 Interactive Observed 지연과 분리하고 등급 계산에서 제외했습니다.
- `PARTIAL_ENGINE`, `PARTIAL_OUTPUT` 등의 내부 상태는 사용자 출력에서 `PARTIAL`로 정규화됩니다.

## 보존 원칙
- Schema1 보존
- Paper 20
- Shadow 60
- Live Trading OFF
- 기존 명령 341개 보존
- 기존 학습 데이터 및 저장 경로 변경 없음

## 검증
- Python compile PASS
- Import PASS
- Preflight PASS
- Pytest 71/71 PASS
- Command Registry 341/341
- Callable 341/341
- Help/Commands coverage 341/341

## 판정
개발 릴리즈입니다. Railway Startup, 실제 Telegram 송수신, Scheduler, Watchdog, SIGTERM, 장시간 Runtime 검증 전에는 LTS Candidate로 선언하지 않습니다.
