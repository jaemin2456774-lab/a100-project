# S50 패치 설치 안내

1. 현재 Railway GitHub 저장소를 백업합니다.
2. ZIP을 풀어 기존 파일 위에 덮어씁니다.
3. 기존 `/data`, 환경변수, 데이터베이스 및 학습 데이터는 삭제하지 않습니다.
4. GitHub에 변경 파일을 반영하고 Railway 배포 완료를 기다립니다.
5. 시작 로그에서 `A100 V116.1 DEV S50` 및 등록 명령 341을 확인합니다.
6. 아래 명령을 순서대로 실행합니다.

```
/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/errors
```

성공 기준: 실제 후보 심볼 표시, Direction과 Decision 분리, Missing Evidence 압축, Explain/Consensus 점수 일치, 신규 TypeError/KeyError/AttributeError 없음.
