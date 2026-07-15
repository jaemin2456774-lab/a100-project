# S2.18.0 설치 안내

1. Railway 프로젝트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
2. `/data`, 환경변수, 설정 파일과 기존 학습 데이터는 삭제하거나 초기화하지 않습니다.
3. 재배포 후 시작 로그에서 `S2.18.0`, 명령 341개, Startup Preflight PASS를 확인합니다.
4. 아래 명령을 순서대로 실행합니다.

```
/version
/versionaudit
/status
/status
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/ltscertification
/pipelinetrace
/commandperformance
/errors
```

## 합격 기준

- 재시작 루프 및 신규 RuntimeError 없음
- Registry/Callable/Expected Commands 341/341
- Version Source SINGLE PASS
- Runtime State SINGLE, Evidence Source SINGLE, Formatter UNIFIED 표시
- 동일 Snapshot ID에서 Runtime score와 Gate 값 일치
- `/runtimehealth`, `/releasegate`, `/status`가 사용자 요청에서 저장소 전체 스캔을 수행하지 않음
- 실제 데이터 기준 미달 Gate의 BLOCKED 표시는 정상
