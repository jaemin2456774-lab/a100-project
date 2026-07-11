A100 V88 STABLE ENGINE 배포 안내

GitHub 저장소 최상위에 아래 파일을 올리세요.
- main.py
- requirements.txt
- render.yaml (Render 사용 시; Railway에서는 참고용)
- README_V88_KR.txt
- CHANGELOG_V88.txt

Railway Start Command:
python -u main.py

정상 시작 로그:
A100 V88 STABLE ENGINE worker running...
A100 V88 required command check: OK
A100 V88: Telegram single polling started

텔레그램 권장 테스트:
/help
/selfcheck
/health
/datastatus
/v88 BTC
/decision BTC
/setup BTC
/conviction BTC
/quality BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
/watchlist
/errors

주의:
기존 main.py를 삭제한 뒤 이 ZIP의 main.py를 같은 파일명으로 업로드하세요.
Railway에서 최신 커밋을 배포하고 위 시작 로그를 확인하세요.
