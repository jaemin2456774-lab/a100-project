# Railway 설치 및 QA

1. 패치의 `main.py`로 기존 파일을 덮어씁니다.
2. 기존 `/data` 볼륨과 환경변수를 그대로 유지합니다.
3. Railway에서 새 배포를 실행합니다.

## 검증 명령
```
/version
/buildinfo
/runtimehealth
/versionaudit
/versionaudit
/papershadow
/papershadowperformance
/errors
```

## 기대 결과
- Registry 341/341
- Current Engine E2E Same-ID PASS
- Historical Baseline No-Growth PASS
- 첫 `/versionaudit`: Baseline State CREATED 또는 ACTIVE
- 두 번째 `/versionaudit`: Baseline State ACTIVE
- Post-baseline Delta 모두 0 이하
- Errors 0
