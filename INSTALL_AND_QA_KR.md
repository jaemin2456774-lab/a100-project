# Railway 설치 및 QA

기존 프로젝트 루트의 `main.py`만 덮어씁니다. `/data`와 환경변수는 유지합니다.

## 배포 후 명령
```
/version
/buildinfo
/papershadowperformance
/papershadowperformance
/runtimehealth
/versionaudit
/papershadow
/coverageplan
/errors
```

## 기대 결과
- `/buildinfo`: Running `V116.2-RC1.3`, RC1.3 Build ID
- 구형 S59 함수명은 `Implementation provenance`로만 표시
- `/coverageplan`: 헤더는 `V116.2 RC1.3`, S59.0.2는 `Module provenance`로만 표시
- `/papershadowperformance` 첫 실행 2000ms 이하
- 두 번째 즉시 실행: Snapshot Read에 가까운 값이 0ms, Cache H 증가, 2000ms 이하
- Registry 341/341, Error 0
