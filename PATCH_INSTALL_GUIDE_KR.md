# S2.17.9 패치 설치 안내

1. ZIP을 풉니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 영구 볼륨과 환경변수는 변경하지 않습니다.
4. Railway 배포 완료 후 아래 명령을 순서대로 실행합니다.

```
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- 버전 `V116.0-LTS-S2.17.9`
- Registry/Callable/Route 341/341
- `Operational Hit Rate` 표시
- `/releasegate`와 `/versionaudit`의 Snapshot ID 및 Unified Hash 일치
- 신규 120초 timeout 없음
