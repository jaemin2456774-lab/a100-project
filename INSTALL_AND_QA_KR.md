# 설치 및 QA

1. 패치를 기존 방식으로 적용하고 Railway를 재배포합니다.
2. `/version`, `/buildinfo`에서 RC2.4.3을 확인합니다.
3. `/commandcert autorun` 실행 후 `/commandcert status`로 Batch가 계속 증가하는지 확인합니다.
4. 중단 시험은 `/commandcert stop`으로만 수행합니다. 상태에 `Stop reason USER_COMMAND`가 표시되어야 합니다.
5. 재시작 시 미완료 Batch부터 재검수되는지 확인합니다.

검증 명령:
```
/version
/buildinfo
/commandcert autorun
/commandcert status
/commandcert status
/commandcert stop
/commandcert status
/errors
```
