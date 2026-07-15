# S2.17.17 패치 설치 안내

1. 기존 GitHub 프로젝트의 `main.py`를 이 패치의 `main.py`로 덮어씁니다.
2. `/data`, 환경변수, Railway Volume은 삭제하거나 초기화하지 않습니다.
3. GitHub 커밋 후 Railway 배포가 완료될 때까지 기다립니다.
4. 배포 후 아래 명령을 순서대로 실행합니다.

```text
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- 버전 `V116.0-LTS-S2.17.17`
- Registry/Callable/Runtime Route 341/341
- `RUNTIME SCORE EXPLAIN ENGINE V6`
- `EVIDENCE ETA PREDICTOR V2`
- `MANDATORY GATE ACTION PLANNER V4`
- `LTS CERTIFICATION PROGRESS V2`
- `FINAL RECOMMENDATION V2`
- `/errors` 신규 오류 0건
