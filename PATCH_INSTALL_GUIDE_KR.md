# S59.7.2 Railway 설치 및 검증 가이드

1. 현재 Railway 배포본과 `/data` 볼륨을 백업합니다.
2. 패치의 `main.py`만 프로젝트의 기존 `main.py`에 덮어씁니다.
3. 기존 `/data`, 환경변수, Learning/Runtime 파일을 삭제하거나 초기화하지 않습니다.
4. Railway에서 재배포합니다.
5. 시작 로그에서 아래 문구를 확인합니다.

```text
A100 V116.1 DEV S59.7.2 ledger compatibility recovery: PASS
```

6. 아래 명령을 순서대로 실행합니다.

```text
/version
/versionaudit
/engineaudit
/commandcert
/commandmatrix
/crossengineaudit
/evidencereplay
/rcpreflight
/verifyall
/errors
```

## 정상 기대값

- Registry 341/341
- Runtime Identity PASS
- Authoritative Routes PASS
- Matrix 341
- 실행한 명령은 `run Y` 또는 실행 수 증가
- `ledger root must be dict, got list` 오류 0건
- Replay/Drift는 복구된 실제 증거에 따라 PASS, REVIEW 또는 MEASURING
- 24h/72h/7d는 실제 시간이 지나기 전 MEASURING
