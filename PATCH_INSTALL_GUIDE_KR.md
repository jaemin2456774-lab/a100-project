# S56.1 패치 설치 안내

1. ZIP의 `main.py`를 GitHub 저장소 루트의 기존 `main.py`에 반드시 덮어씁니다.
2. GitHub에서 변경된 `main.py`가 약 3.7MB인지 확인하고 커밋합니다.
3. Railway에서 새 배포가 완료될 때까지 기다립니다.
4. Railway Deploy Logs에서 아래 문자열을 확인합니다.
   - `V116.1-DEV-S56.1 worker running...`
   - `BUILD_ID=S56.1-20260718-BUILD-INTEGRITY-01`
5. Telegram에서 `/version`, `/buildinfo`, `/connectivity`, `/verifyall` 순서로 실행합니다.

`/version`이 S55로 남아 있으면 Railway가 이전 커밋/브랜치를 배포 중인 것이므로 Railway 서비스의 Source Repository와 Branch를 확인해야 합니다.
