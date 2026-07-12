# V92.8 설치 후 확인 체크리스트

1. 시작 로그에 `A100 V92.8 COMMAND INTEGRITY & VERSION SYNC worker running...` 확인
2. `/help`에서 V92.8 및 Shadow 명령 4종 확인
3. `/commands V92`에서 V92.8 확인
4. `/papershadowstatus` 정상 응답
5. `/papershadowpositions` 정상 응답
6. `/papershadowhistory` 정상 응답 또는 이력 없음 안내
7. `/papershadowstats` 정상 응답
8. `/intelligence BTC`에서 Raw/Calibrated/Gain 및 Learning Progress 확인
9. `/dashboard BTC`, `/final BTC`에서 V92.8 확인
10. `/memory`, `/review`, `/consensus BTC`, `/gold BTC`, `/ai` 회귀 확인
11. 기존 Paper/Shadow OPEN 및 청산 이력 복원 확인
12. 중복 응답, 출력 잘림, 명령 미지원 메시지 여부 확인
