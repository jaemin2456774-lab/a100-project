# RC4.9.7 설치 후 Telegram 검수 순서

아래 명령을 한 메시지에 순서대로 입력하거나 각각 실행하십시오.

/version
/status
/status
/dashboard btc
/releasegate
/performanceaudit
/commandcert
/commandcert warn engine
/commandcert warn adaptiveconfidence

## 필수 확인
- 모든 화면 버전이 RC4.9.7
- 첫 `/status`: MISS(cold_start 가능)
- 두 번째 `/status`: HIT, Age, TTL 남음 표시
- `/performanceaudit`: Queue Wait / Engine / Telegram Send / End-to-End 분리
- Grade Reasons / Targets 표시
- `/commandcert`: Top Causes 요약
- 원인별 drill-down 결과가 1~2화면 내 출력
