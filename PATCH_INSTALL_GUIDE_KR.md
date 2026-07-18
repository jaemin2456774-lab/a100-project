# S56.2 설치 안내

1. ZIP을 압축 해제합니다.
2. 저장소 루트의 기존 `main.py`를 ZIP의 `main.py`로 완전히 덮어씁니다.
3. Git commit/push 후 Railway 최신 배포가 완료될 때까지 기다립니다.
4. Railway 시작 로그에서 아래 문구를 확인합니다.

```
V116.1-DEV-S56.2 worker running...
BUILD_ID=S56.2-20260718-EXEC-ORDER-IDENTITY-01
A100 V116.1 DEV S56.2 executable order recovery: PASS
A100 V116.1 DEV S56.2 runtime identity audit: PASS
```

5. 텔레그램에서 실행합니다.

```
/version
/buildinfo
/connectivity
/connectivity detail
/verifyall
/errors
```

정상이라면 `/version`, `/buildinfo`, `/verifyall`이 모두 S56.2를 표시합니다.
