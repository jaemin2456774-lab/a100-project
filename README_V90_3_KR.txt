A100 V90.3 STABILITY & SHARED CONTEXT

배포 파일
- main.py
- requirements.txt
- render.yaml

Railway 설정
- Build Command: pip install -r requirements.txt
- Start Command: python -u main.py

주요 수정
1. V90.2 기존 명령 레지스트리 전체 유지
2. Binance 심볼 목록 시작 시 자동 보정 및 하루 1회 갱신
3. API 실패 시 기존 심볼 캐시 유지
4. 동일 심볼 분석 결과 60초 공통 캐시 적용
5. /health에 심볼 수, 캐시 적중률, DB/Volume 상태 추가
6. /selfcheck의 Binance 심볼 검사를 실제 캐시 기준으로 수정
7. /legacycheck 핵심 명령 범위 확대
8. 단일 명령 디스패처와 대기 명령 보존 유지

배포 후 확인 순서
/selfcheck
/legacycheck
/commands
/health
/v90 BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
