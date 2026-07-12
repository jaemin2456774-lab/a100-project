# V92.5 설치 후 테스트 체크리스트

1. 기존 데이터 파일과 환경변수를 그대로 유지한 채 ZIP을 배포합니다.
2. 시작 로그에서 `A100 V92.5 AI DECISION INTELLIGENCE ENGINE worker running...`을 확인합니다.
3. 시작 로그에서 `learning report loop started (4h)`를 확인합니다.
4. `/help` 실행 후 V92.5 표시와 `/intelligence`, `/learningstatus` 안내를 확인합니다.
5. `/commands V92` 실행 후 새 명령 4개가 포함되어 있는지 확인합니다.
6. `/intelligence BTC`와 `/decisionai BTC`가 동일하게 응답하는지 확인합니다.
7. `/learningstatus`와 `/learningreport`가 동일하게 응답하는지 확인합니다.
8. `/memory`, `/review`, `/dashboard BTC`, `/final BTC`, `/gold BTC`, `/topscore`를 실행하여 기존 기능 회귀 여부를 확인합니다.
9. 기존 OPEN 및 평가 완료 데이터 건수가 설치 전과 동일한지 확인합니다.
10. 4시간 후 자동 학습 리포트가 `TELEGRAM_CHAT_ID` 채팅방에 한 번만 도착하는지 확인합니다.
11. 재배포 후 중복 리포트 또는 중복 polling이 없는지 확인합니다.
12. 캡처 시 전체 화면을 보내면 명령 누락, 잘림, 응답 중복, 데이터 이상, 버전 불일치를 우선 검토합니다.
