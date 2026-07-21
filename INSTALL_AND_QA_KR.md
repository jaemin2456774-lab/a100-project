# A100 V118.0 RC3.5 설치 및 검수

1. 기존 저장 데이터와 Railway 환경변수를 유지합니다.
2. 패치의 `main.py`를 저장소에 덮어씁니다.
3. Railway에 배포하고 신규 컨테이너가 안정적으로 실행되는지 확인합니다.

## 검수 명령

```text
/version
/buildinfo
/versionaudit
/commandcert
/commandmatrix
/trustgate
/intelligencescore
/performance
/errors
```

## 확인 기준

- Registry 341/341
- Architecture Guard PASS
- Version Audit PASS
- `/buildinfo`에 recovery 내부 5개 phase와 render_warmup 표시
- 배포 후 핵심 명령이 Cache HIT로 응답
- `/commandcert` 진단 TTL이 최대 300초로 표시
- `/errors`에 배포 후 신규 Traceback 없음
