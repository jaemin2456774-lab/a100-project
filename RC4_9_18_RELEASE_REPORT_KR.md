# A100 V116.0 RC4.9.18 개발 릴리즈 보고서

## 목표
LTS Final 직전의 출력·도움말·성능 통계·명령 경로 인증을 최종 안정화합니다.

## 수정 사항
- 성능 감사의 `Recent 30` 계산을 값 정렬 후 상위 30개가 아니라 **기록 시간순 최근 30개**로 수정했습니다.
- P95 계산을 명시적인 nearest-rank 방식으로 통일했습니다.
- `/help`, `/commands` 장문 출력을 줄 단위 3,600자 안전 분할로 변경하여 명령 설명 중간 절단을 방지했습니다.
- 341개 명령에 대해 callable/signature/source compile/source fingerprint 기반 읽기 전용 Route Certification을 추가했습니다.
- Structural Certification과 실제 Telegram Live Evidence를 분리 표시하여 Dry Probe를 실제 E2E 실행으로 오인하지 않도록 수정했습니다.
- VersionManager, Registry, Help/Commands, Preflight를 RC4.9.18로 동기화했습니다.

## 보존 사항
- Schema 1 유지
- Paper 20 / Shadow 60 유지
- Live Trading OFF
- 기존 데이터 및 학습 데이터 보존
- 활성 명령 341개 유지

## 검증 결과
- Python compile: PASS
- Preflight: PASS
- Registry: 341/341
- Read-only Route Certification: 341/341, error 0
- 기존 회귀 테스트 + RC4.9.18 신규 테스트: 전체 항목 PASS

## 주의
Route Certification은 안전한 구조·소스 경로 검증입니다. 실제 Telegram 송수신 E2E 증거는 설치 후 명령 캡처로 별도 확인해야 합니다.
