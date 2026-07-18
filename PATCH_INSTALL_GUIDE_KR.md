# S56 증분 패치 설치 안내

1. Railway 연결 GitHub 저장소의 프로젝트 루트에 ZIP 내부 파일을 덮어씁니다.
2. 기존 `/data`, 환경변수, 설정 및 학습 데이터는 삭제하지 않습니다.
3. Railway 배포 완료 후 다음 명령을 실행합니다.

```text
/version
/verifyall
/connectivity
/connectivity detail
/verifyall detail
/errors
```

확인 기준:
- `/evidence`가 Registry 외 dispatcher route임에도 PASS로 표시
- Connected N/16 및 Missing 목록 확인
- 네 대상 producer의 Runtime/Schema/Aggregator/Recovery 단계 확인
- Synthetic completion OFF, Gate mutation NONE, Registry 341/341
