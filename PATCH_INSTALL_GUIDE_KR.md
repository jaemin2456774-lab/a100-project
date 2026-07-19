# S59.7.1 증분 패치 설치 및 Railway 검증

## 설치
1. 현재 저장소와 Railway Volume 데이터를 백업합니다.
2. ZIP의 `main.py`만 프로젝트 루트의 기존 파일에 덮어씁니다.
3. 기존 `/data`, Runtime, Learning, 환경설정 파일은 삭제하거나 초기화하지 않습니다.
4. GitHub 반영 후 Railway에서 재배포합니다.

## 중요한 환경변수
다음 값은 실제 검증을 완료한 항목만 `true`로 설정합니다. 검증 전에는 설정하지 않습니다.
- `A100_RUNTIME_FIRST_CERTIFIED`
- `A100_GATE_FORMULA_UNCHANGED_CERTIFIED`
- `A100_RUNTIME_DATA_PRESERVED_CERTIFIED`
- `A100_LEARNING_DATA_PRESERVED_CERTIFIED`
- `A100_LIVE_TRADING_OFF_CERTIFIED`

미설정 상태에서는 관련 Freeze 항목이 PASS가 아니라 `MEASURING`으로 유지됩니다.

## 배포 직후 캡처 명령
```text
/version
/status
/runtimehealth
/buildinfo
/routeraudit
/versionaudit
/engineaudit
/commandcert
/commandmatrix
/regressionguard
/crossengineaudit
/evidencereplay
/rcpreflight
/verifyall
/errors
```

## Railway 로그 확인 키워드
```text
V116.1-DEV-S59.7.1
S59.7.1-20260719-RC-CERTIFICATION-TRUTHFULNESS-RUNTIME-PERFORMANCE-HOTFIX-01
registered commands: 341
worker running
Traceback
RuntimeError
TypeError
```

배포 직후 24h/72h/7d는 반드시 `MEASURING`이어야 정상입니다.
