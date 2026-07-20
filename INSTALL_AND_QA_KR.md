# Railway 설치 및 QA

기존 프로젝트의 `main.py`만 덮어쓰고 기존 `/data`와 환경변수는 보존합니다.

검증 순서:

```text
/version
/buildinfo
/runtimehealth
/versionaudit
/commandcert batch 1
/commandcert batch 1 run
/commandcert status
/commandcert
/commandmatrix
/errors
```

Batch 1이 정상 완료되면:

```text
/commandcert autorun
/commandcert status
```

중지:

```text
/commandcert stop
```

기대 결과:
- Registry 341/341
- `batch 1 run`이 기본 Summary가 아니라 START/COMPLETE 메시지 출력
- `status`에 RUNNING/COMPLETED, Batch, Current/Last Command, Heartbeat 표시
- Completed 수 증가
- 실제 증거 충족 명령만 PARTIAL에서 PASS로 승격
