# S48 패치 설치 안내

1. 기존 Railway 프로젝트 데이터와 환경변수는 유지합니다.
2. ZIP의 파일을 저장소 루트에 덮어씁니다.
3. GitHub에 커밋·푸시한 뒤 Railway 배포가 완료될 때까지 기다립니다.
4. Startup 로그에서 S48 preflight와 producer ACTIVE 로그를 확인합니다.
5. 아래 명령을 순서대로 실행합니다.

/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/releasegate detail
/errors

성공 확인 핵심:
- Evidence Runtime S48
- Funding/OI/Volume/Volatility/Momentum ON 여부
- Coverage가 S47보다 상승했는지
- 신규 NameError/KeyError/TypeError/ImportError/AttributeError 없음
- 메모리 Guard ACTIVE 및 재시작 급증 없음

ReleaseGate Structural FAIL은 이번 패치에서 강제 PASS 처리하지 않습니다.
