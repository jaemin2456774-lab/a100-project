# S51 증분 패치 설치 안내

1. Railway에 연결된 GitHub 저장소에서 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. 기존 `/data`, 환경변수, 설정 파일은 변경하거나 삭제하지 않습니다.
3. 커밋·푸시 후 Railway 배포가 완료될 때까지 기다립니다.
4. Startup 로그에서 `A100 V116.1 DEV S51 ... PASS`와 Registry 341을 확인합니다.
5. 아래 명령을 순서대로 실행해 캡처합니다.

`/version`
`/status`
`/runtimehealth`
`/evidence`
`/releasegate`
`/releasegate detail`
`/sniper`
`/sniper detail`
`/ultimate`
`/ultimate detail`
`/errors`

주의: 데이터·설정 삭제, 캐시 강제 초기화, Gate 임계값 변경을 하지 않습니다.
