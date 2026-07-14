# A100 V116.0 RC4.9.19 릴리즈 보고서

## 목적
RC4.9.18의 341개 전체 명령 인증 강도는 유지하면서 `/versionaudit`, `/commandcert` 및 반복 Preflight가 사용자 응답 경로에서 같은 소스 검사를 중복 수행하던 병목을 제거했습니다.

## 핵심 변경
- 코드/Registry 지문 기반 Certification Cache 도입
- 341개 Handler source inspection 및 compile 인증을 코드 지문당 1회만 수행
- 일반 `/versionaudit`, `/commandcert`는 검증된 Snapshot을 사용해 즉시 응답
- `/commandcert deep`에서만 전체 인증을 강제로 갱신
- Deep 검사는 `asyncio.to_thread`로 Telegram event loop와 분리
- Preflight 결과도 코드 지문 기준 캐시하여 반복 호출 비용 제거
- Registry가 변경되면 지문이 달라져 캐시가 자동 무효화됨
- Schema 1, Paper 20, Shadow 60, Live OFF 및 기존 학습 데이터 보존

## 성능 검증
- 최초 전체 Preflight: 약 1.2초(환경 의존, 시작 시 1회)
- 반복 Preflight: 약 0.1ms
- 반복 Certification 조회: 약 0.1ms
- 전체 pytest: PASS
- Registry/Route Certification: 341/341, error 0

## 설계 원칙
속도를 위해 검증 범위를 줄이지 않았습니다. 동일 코드를 반복 검사하지 않는 방식으로 속도와 인증 신뢰성을 함께 유지합니다.
