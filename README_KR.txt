A100 v83 AI TRADING ASSISTANT ENGINE

교체 파일
- main.py
- requirements.txt

v83 핵심 기능
- 최종등급 A+ / A / B / C / D
- LONG/SHORT 퍼센트 게이지
- 현재 단계 1~5 시각화
- 진입 제한 사유 우선순위
- 자동 체크리스트
- 추천 행동 및 예상 재검증 시간
- 점수 변화 추적: 1시간 / 4시간 / 24시간
- PostgreSQL + Railway Volume 이중 저장
- 재배포/재시작 후 점수 이력 유지
- 신규 명령어 /scorehistory BTC

확인 명령어
/health
/datastatus
/quality BTC
/why BTC
/scorehistory BTC

정상 상태
- PostgreSQL: 정상
- Railway Volume: 정상
- 점수 이력: 활성

주의
확률, 예상 손익비, 대기시간, 성공 참고값은 실측 수익이나 승률 보장값이 아닙니다.
주문 실행 기준으로 단독 사용하지 마세요.
