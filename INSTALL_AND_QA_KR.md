# A100 V118.0 RC3.6 설치 및 QA

기존 저장소에 패치 파일을 덮어쓴 뒤 Railway에서 재배포합니다. 데이터 볼륨과 환경변수는 변경하지 않습니다.

## 1차 검수

```text
/version
/buildinfo
/versionaudit
/performance
/errors
```

`/buildinfo`에서 다음을 확인합니다.

```text
Registry 341/341
Architecture Guard PASS
recovery_matrix_refresh 0.0ms
recovery_matrix_reuse 수 ms 수준
```

첫 배포에서는 저장 Matrix Snapshot이 없을 수 있으므로 `DEFERRED_COLD_START`가 정상입니다. 이후 백그라운드 갱신이 완료되면 `/data/v118_matrix_snapshot.json`이 생성되고 다음 재시작부터 `PERSISTED_HIT`가 사용됩니다.

## Cache 검수

15분 안에 각 명령을 두 번 실행합니다.

```text
/commandcert
/commandcert
/commandmatrix
/commandmatrix
/trustgate
/trustgate
/intelligencescore
/intelligencescore
/performance
```

두 번째 실행은 `Cache HIT`여야 합니다. `/performance`에서 Hits/Misses, Last HIT, Entries, TTL을 확인합니다.
