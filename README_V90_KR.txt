A100 V90 FULL LEGACY INTEGRATION ENGINE

이번 버전은 V89에 최신 기능만 추가한 것이 아니라,
현재 소스에 남아 있는 과거 CommandHandler와 handlers 목록을 전수 분석하여
기존 명령을 정적 레지스트리로 다시 등록했습니다.

통합 명령 수: 104개
과거 소스에서 확인된 명령: 93개
빌드 시 콜백 누락: 0개

배포 파일
- main.py
- requirements.txt
- render.yaml
- README_V90_KR.txt
- CHANGELOG_V90.txt
- COMMAND_AUDIT_V90.json

GitHub 적용
1. 기존 main.py 내용을 V90 main.py로 완전히 교체합니다.
2. requirements.txt와 render.yaml도 함께 업로드합니다.
3. Railway Start Command:
   python -u main.py
4. 최신 커밋을 배포합니다.

정상 시작 로그
A100 V90 FULL LEGACY INTEGRATION ENGINE worker running...
A100 V90 registered commands: 104
A100 V90 full legacy command check: OK

배포 후 확인
/selfcheck
/legacycheck
/commands
/health
/v90 BTC
/quality BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
/datastatus
/errors

중요
정적·문법 검사는 완료했지만 실제 Binance, CoinGlass, Telegram,
PostgreSQL 응답은 배포 환경의 키·네트워크·데이터 상태에 따라 달라집니다.
