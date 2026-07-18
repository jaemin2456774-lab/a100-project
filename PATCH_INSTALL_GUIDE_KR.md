# S45 패치 설치 안내 (Railway)

1. 현재 GitHub 저장소에서 `main.py`를 이 패치의 파일로 덮어씁니다.
2. 문서 파일은 배포 필수 파일이 아니며 기록용입니다.
3. GitHub에 커밋·푸시합니다.
4. Railway 배포가 완료될 때까지 기다립니다.
5. Railway 로그에서 아래 문구를 확인합니다.

- `A100 V116.1 DEV S45 worker running...`
- `A100 V116.1 DEV S45 LONG/SHORT Runtime Integration audit: PASS`
- `scan path: FILTERED RUNTIME -> RAW RUNTIME QUALITY HOLD`
- `synthetic evidence/pass: DISABLED`
- `live trading: OFF`

## 배포 후 1차 명령

/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/releasegate detail
/errors

## 2차 반복 테스트

10~15초 안에 다음을 다시 실행합니다.

/ultimate
/ultimate detail
/god

확인 항목: `CACHE_` source 표시, 방향 일관성, Consensus/Final AI 모순 여부, 메모리 급증, 신규 오류.
