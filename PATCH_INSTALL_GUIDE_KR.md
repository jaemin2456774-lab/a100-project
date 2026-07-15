# S2.17.1 패치 설치 안내

1. ZIP 압축을 풉니다.
2. 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 교체합니다.
3. GitHub에 커밋한 뒤 Railway에서 최신 커밋을 재배포합니다.
4. 정상 로그 순서:
   - `Health server listening on port 8080`
   - `A100 V116.0-LTS-S2.17.1 ... worker running...`
   - `A100 V91 preflight: OK`
   - `Telegram single polling started`
   - `post-start certification warmup: OK`
5. 배포 후 `/version`, `/status`, `/versionaudit`, `/pipelinetrace`, `/errors`를 확인합니다.

데이터 디렉터리, Schema, Paper/Shadow 수량 및 Live 설정은 변경하지 않습니다.
