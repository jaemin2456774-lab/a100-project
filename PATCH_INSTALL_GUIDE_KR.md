# S2.15 패치 설치 안내

1. 배포 중인 GitHub 저장소의 루트 `main.py`를 백업합니다.
2. 이 패키지의 `main.py`로 저장소 루트 파일을 교체합니다.
3. Commit 후 Railway 재배포를 기다립니다.
4. 아래 명령을 순서대로 실행합니다.

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

## 정상 적용 기준
- `/version`: `V116.0-LTS-S2.15`
- 네 통합 화면의 `Snapshot ID`와 Runtime Score가 동일한 스냅샷 구간에서 일치
- `/runtimehealth`: `Pipeline live source PASS`
- `/releasegate`: 각 Gate의 Current / Target / Gap 표시
- `/pipelinetrace`: PASS
- `/errors`: 0

기존 데이터, 환경변수, 볼륨 및 Schema는 변경하지 않습니다.
