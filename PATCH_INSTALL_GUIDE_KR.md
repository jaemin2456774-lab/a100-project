# S2.14 패치 설치 안내

1. 배포 전 현재 `main.py`를 백업합니다.
2. 이 패키지의 `main.py`를 GitHub 저장소 루트의 `main.py`와 교체합니다.
3. GitHub에 커밋 후 Railway 재배포를 진행합니다.
4. 배포 완료 후 아래 명령을 순서대로 확인합니다.

```text
/version
/status
/runtimehealth
/dashboard btc
/releasegate
/versionaudit
/pipelinetrace
/errors
```

정상 기준:
- `/version`: `V116.0-LTS-S2.14`
- `/runtimehealth`: `UNIFIED RUNTIME SCORE ENGINE`
- `/dashboard`: `LTS FINAL READINESS · UNIFIED`
- `/releasegate`: `RELEASE GATE · UNIFIED CERTIFICATION ENGINE`
- Runtime Score가 Status, Runtime Health, Dashboard, Release Gate에서 동일해야 합니다.
