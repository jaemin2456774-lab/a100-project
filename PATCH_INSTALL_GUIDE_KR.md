# S59.7.4 Railway 설치 가이드

1. 기존 Railway 데이터 볼륨과 환경변수를 보존합니다.
2. 패치의 `main.py`만 프로젝트의 동일 경로에 덮어씁니다.
3. Railway에서 새 배포를 실행합니다.
4. 시작 로그에서 S59.7.4 Build ID와 Registry 341/341을 확인합니다.
5. 다음 명령을 순서대로 실행합니다.

/version
/versionaudit
/evidencereplay
/crossengineaudit
/commandmatrix
/rcpreflight
/verifyall
/errors

정상 기준:
- 모든 현재 인증 화면 버전 S59.7.4
- Version Audit PASS
- Evidence가 존재하면 Replay PASS 100/100
- Telegram TimedOut 반복 없음
- 장시간 인증은 실제 시간이 충족될 때까지 MEASURING
