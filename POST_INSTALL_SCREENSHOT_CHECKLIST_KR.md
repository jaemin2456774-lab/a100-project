# RC4.9.6 설치 후 캡처 체크리스트

아래 순서로 실행하고 결과 화면을 보내주세요.

1. `/version` — RC4.9.6 표시
2. `/status` 두 번 연속 — 첫 실행 MISS, 두 번째 HIT와 Age 표시 확인
3. `/dashboard btc` — 상단 RC4.9.6 및 다음 학습 목표 확인
4. `/releasegate` — LTS Score Progress와 Mandatory Gates 분리 확인
5. `/performanceaudit` — Handler/Queue/End-to-End/Cache 지표 확인
6. `/commandcert` — 요약 출력 확인
7. `/commandcert detail` — 압축 상세 확인
8. `/commandcert warn engine` — 원인 필터 확인

필수 캡처: 1~8 전체. `/status`는 두 결과가 한 화면에 보이도록 캡처합니다.
