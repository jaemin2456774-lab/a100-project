# A100 V116.0 LTS RC4.9.4 개발 릴리스 보고서

## 목표
RC4.9.3의 기능과 Schema 1 데이터를 보존하면서 Telegram 명령 응답 지연과 과도한 출력 문제를 개선한다.

## 핵심 변경
- 전체 명령 공통 Latency Profiler: 최근/평균/최대 실행시간, FAST/NORMAL/SLOW/CRITICAL 기록
- `/commandperformance`, `/latency` 추가: 캐시 적중률과 느린 명령 TOP 15 표시
- Shared State Context: 동일 명령 구간의 `_v91_load_state()` 중복 호출 감소
- Snapshot 기반 TTL Cache
  - Command Certification 60초
  - LTS Certification 30초
  - Regression 60초
  - Shared State 2초
- 무거운 명령 실행 전 즉시 `정밀 검증 중` 응답
- 일반 명령 제한시간 180초 → 120초로 축소하고 오류 격리 유지
- `/commandcert` 기본 요약 8건, `/commandcert detail`로 상세 출력
- `/ltscert` 기본 요약, `/ltscert detail`로 전체 체크 출력
- 기존 Engine, Repository, Snapshot, Pipeline, 학습 데이터 및 Telegram 명령 보존

## 보존 조건
- Schema 1 유지
- Paper 20 유지
- Shadow 60 유지
- Live Trading OFF 유지
- 기존 RC4.9.3 기능 삭제 없음

## 검증 결과
- Python compile: PASS
- RC4.9.4 전용 회귀 테스트: 5/5 PASS
- RC4.9.4 startup preflight: PASS
- Registry sync: PASS
- Cache hit/invalidation test: PASS
- Latency classification test: PASS
- 전체 누적 pytest: 40 PASS / 9 historical version-lock failures

### 누적 pytest 9건 설명
이전 RC4.1~RC4.9.3 테스트 일부가 `V91_VERSION == 과거 버전` 또는 과거 handler identity를 고정 검증하므로 최신 RC4.9.4에서는 의도적으로 실패한다. 기능 회귀나 런타임 실패가 아니라 과거 버전 고정 assertion이다. RC4.9.4 전용 테스트와 최종 startup preflight는 모두 통과했다.

## 설치 후 권장 확인
1. `/version`
2. `/commandperformance`
3. `/commandcert`
4. 같은 명령을 다시 실행해 Cache HIT 확인
5. `/commandcert detail`
6. `/ltscert` 및 `/ltscert detail`
