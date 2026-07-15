# S2.17.13 패치 설치 안내

1. ZIP을 압축 해제합니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 폴더와 Railway Volume은 삭제하지 않습니다.
4. GitHub에 커밋한 뒤 Railway 재배포를 확인합니다.

## 배포 후 확인
```
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- 버전 `V116.0-LTS-S2.17.13`
- Operational Hit Rate와 Overall Hit Rate 분리 표시
- 1h/6h/24h/72h Runtime Score Delta 표시
- Registry/Callable/Runtime Route 341/341
- 신규 timeout 및 runtime error 없음
