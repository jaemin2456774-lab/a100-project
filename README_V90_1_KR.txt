A100 V90.1 COMMAND RELIABILITY ENGINE

이번 버전은 기능을 더 붙이는 버전이 아니라,
명령이 무응답이 되는 구조 자체를 교체한 안정화 버전입니다.

핵심 변경
1. 기존 104개 명령을 모두 V90 레지스트리에 유지
2. CommandHandler 104개 개별 등록을 폐기
3. 단일 명령 디스패처 1개로 모든 명령 처리
4. 여러 줄로 붙여 넣은 명령도 줄별로 실행
5. 한 명령이 오류 나도 다음 명령과 봇 전체는 계속 작동
6. Telegram 재연결 시 대기 명령을 삭제하지 않음
7. /health /selfcheck /legacycheck는 외부 API 없이 즉시 응답
8. 명령별 180초 타임아웃으로 무한 대기 방지

배포 방법
1. GitHub의 기존 main.py를 이 ZIP의 main.py로 완전히 교체
2. requirements.txt와 render.yaml도 함께 교체
3. Railway Start Command:
   python -u main.py
4. 최신 커밋을 배포

정상 시작 로그
A100 V90.1 COMMAND RELIABILITY ENGINE worker running...
A100 V90.1 registered commands: 104
A100 V90.1 dispatcher count: 1
A100 V90.1 registry validation: OK
A100 V90.1: Telegram single polling started

배포 직후 테스트
/health
/selfcheck
/legacycheck
/commands
/v90 BTC
/quality BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
/errors

여러 줄 테스트도 가능
/health
/selfcheck
/legacycheck

주의
GitHub에서 main.py를 덮어쓴 뒤 Railway 배포 로그에 반드시
'V90.1 COMMAND RELIABILITY ENGINE'이 보여야 합니다.
V89 또는 V90 로그가 보이면 이전 파일이 실행 중인 것입니다.
