A100 v87.1 UNIFIED ENGINE

GitHub에는 아래 파일만 유지하세요.
- main.py
- requirements.txt
- render.yaml (사용 중인 경우)
- README.md (선택)

배포 확인 로그:
A100 v87.1 UNIFIED ENGINE worker running...
A100 v87.1 required command check: OK

Telegram 테스트:
/help
/whale87 BTC
/alertplan BTC
/whale87
/alertplan
/quality BTC
/pulse BTC
/risk BTC

핵심 수정:
- 중첩 builder 제거
- 모든 명령어 단일 등록부 통합
- /whale87, /alertplan 실제 등록 보장
- 심볼 생략 시 BTC 기본 적용
- 미등록 명령 무응답 방지
- 필수 명령 등록 자동 검증
- 명령 실행 로그 추가
- PostgreSQL, Railway Volume, 학습 및 v87 기능 유지
