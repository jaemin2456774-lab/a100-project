# 설치 및 QA

1. main.py를 배포합니다.
2. `/version`, `/buildinfo`로 RC2.4.7을 확인합니다.
3. `/versionaudit`을 두 번 실행합니다.
4. `/commandcert batch 1 run` 후 `/commandcert status`를 실행합니다.
5. Mutation commands, Reconciled PASS, Historical delta를 확인합니다.
6. `/errors`에서 DUPLICATE_POSITION Expected Guard가 제외됐는지 확인합니다.
