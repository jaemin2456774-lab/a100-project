# A100 V116.0 RC4.9.17 개발 릴리즈 보고서

## 목적
RC4.9.16 실환경 캡처에서 확인된 잔존 문제를 수정합니다.

- Batch/Plain Text에서 HTML 태그 노출 방지
- Dynamic Help와 Command Index의 RC4.2 하드코딩 제거
- 341개 명령 경로를 순환 점검하는 안전한 Read-only Dry Route Probe 추가
- Release Gate 학습 우선순위 추천 추가
- Performance Audit의 최근 P95와 누적 P95 분리

## 보존 원칙
- Schema 1 보존
- Paper 20 유지
- Shadow 60 유지
- Live Trading OFF
- 기존 학습 데이터와 기능 보존

## 검증 결과
- Python Compile: PASS
- Pytest: 74/74 PASS
- Registry: 341/341
- Handler: 341/341
- Help Coverage: 341/341
- Preflight: PASS

## Runtime Evidence 주의
`Background dry route probe`는 실제 Telegram 송수신과 구분됩니다. `/commandcert deep`을 실행할 때마다 최대 50개 활성 handler의 callable/source/registry 경로를 안전하게 순환 검사합니다. 실제 Telegram E2E 수치는 별도로 표시합니다.
