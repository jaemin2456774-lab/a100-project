# 설치 및 Railway QA

기존 프로젝트의 `main.py`를 이 패치의 `main.py`로 덮어쓴 뒤 Railway에 배포합니다. 기존 `/data`, 환경변수와 학습 데이터는 삭제하지 않습니다.

## 배포 후 실행 순서

```text
/version
/buildinfo
/runtimehealth
/versionaudit
/papershadowperformance
/papershadowperformance
/papershadow
/coverageplan
/errors
```

## 기대값
- Registry 341/341
- Version Audit PASS
- Runtime Identity PASS
- `/papershadowperformance` 헤더 V116.2 RC1.6
- 출력 진단에 `Bounded QA Cache` 표시
- 연속 호출에서 HIT, Snapshot Read 약 0ms, Handler Total 2000ms 이하
- V88 오류 없음
