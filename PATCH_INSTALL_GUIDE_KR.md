# S56.3 증분 패치 설치 안내

1. ZIP을 해제합니다.
2. 저장소 루트의 기존 `main.py`를 새 `main.py`로 덮어씁니다.
3. 변경 파일을 GitHub에 commit/push 합니다.
4. Railway 최신 배포가 완료될 때까지 기다립니다.
5. 시작 로그에서 `V116.1-DEV-S56.3 worker running`과 `DEV fail-safe: CONTINUE` 또는 identity audit PASS를 확인합니다.

## 배포 후 확인

```text
/version
/buildinfo
/connectivity
/connectivity detail
/verifyall
/errors
```

Identity 항목이 불일치해도 DEV에서는 경고를 기록하고 계속 실행합니다. LTS Gate 계산식과 실제 Evidence 값은 변경하지 않습니다.
