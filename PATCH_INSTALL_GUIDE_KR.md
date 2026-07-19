# S59.7.5.3 패치 설치 안내

1. Railway에 현재 저장소 백업 또는 커밋을 남깁니다.
2. ZIP의 `main.py`를 저장소 루트의 기존 `main.py`에 덮어씁니다.
3. 기존 `/data`, 환경변수, Runtime/Learning 파일은 삭제하지 않습니다.
4. Railway 재배포 후 아래 명령을 순서대로 실행합니다.

```text
/version
/versionaudit
/runtimehealth
/status
/commandmatrix
/crossengineaudit
/evidencereplay
/rcpreflight
/releasegate
/errors
```

우선 기대 결과:
- Registry 341/341
- Version Audit PASS
- Runtime Identity PASS
- `/crossengineaudit` NameError 없음
- 모든 진단 라벨 S59.7.5.3
