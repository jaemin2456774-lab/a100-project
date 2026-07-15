# S2.17.15 패치 설치 안내

1. Railway/GitHub에 있는 기존 프로젝트의 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. `/data` 폴더와 환경변수는 삭제하거나 초기화하지 않습니다.
3. GitHub 커밋 후 Railway 배포가 완료될 때까지 기다립니다.
4. 시작 로그에서 `V116.0-LTS-S2.17.15`와 `startup preflight: PASS`를 확인합니다.
5. 텔레그램에서 아래 순서로 실행합니다.

```text
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- `/releasegate`와 `/versionaudit`의 Snapshot ID와 Unified Hash가 동일합니다.
- `RUNTIME EVIDENCE CORRELATION V3`의 샘플 수가 `RUNTIME WINDOW ENGINE V3`의 72h 샘플 수와 같습니다.
- 1h ≤ 6h ≤ 24h ≤ 72h 순서로 샘플 수가 증가하거나 같습니다.
- `Total Hits + Total Misses = Total Requests`가 성립합니다.
- Overall Hit Rate와 Operational Hit Rate가 별도로 표시됩니다.
- `/errors`에 신규 timeout 또는 S2.17.15 consistency 오류가 없어야 합니다.
