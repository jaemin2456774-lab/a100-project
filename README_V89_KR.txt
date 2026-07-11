A100 V89 ULTIMATE STABLE ENGINE

배포 파일
- main.py
- requirements.txt
- render.yaml
- README_V89_KR.txt
- CHANGELOG_V89.txt

GitHub 적용
1. 기존 main.py를 삭제하거나 내용 전체를 교체합니다.
2. 이 압축파일의 main.py를 저장소 최상위에 업로드합니다.
3. requirements.txt도 함께 교체합니다.
4. Railway Start Command는 다음을 유지합니다.
   python -u main.py
5. 최신 커밋을 배포합니다.

정상 시작 로그
A100 V89 ULTIMATE STABLE ENGINE worker running...
A100 V89 required command check: OK
A100 V88: Telegram single polling started

배포 후 테스트 순서
/selfcheck
/health
/v89 BTC
/decision BTC
/setup BTC
/conviction BTC
/watchlist
/quality BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
/errors

이번 버전은 정상 명령 실행 뒤 '지원하지 않는 명령어'가 중복 출력되는 문제를 제거했습니다.
또한 Result 객체를 dict처럼 호출하여 발생한 AttributeError를 호환 계층으로 차단합니다.
