# S2.17.4 패치 설치 안내

1. ZIP을 압축 해제합니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 교체합니다.
3. `data/` 및 Railway 영구 볼륨은 삭제하지 않습니다.
4. GitHub 커밋 후 Railway 재배포를 진행합니다.

정상 시작 로그:
- `Health server listening on port 8080`
- `A100 V116.0-LTS-S2.17.4 ... worker running...`
- `A100 V91 startup preflight: OK (bounded)`
- `Telegram single polling started`
- `certification snapshot warmup: OK`

배포 후 확인:
`/version`, `/releasegate`, `/versionaudit`, `/errors`
