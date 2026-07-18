# A100 V116.1 DEV S44.1 긴급 설치 안내

## 원인
`Path` import 누락으로 Railway 시작 단계에서 `NameError`가 발생했습니다.

## 설치
이 ZIP의 파일을 저장소 루트에 덮어쓴 뒤 GitHub에 커밋/푸시합니다. 기존 `/data`, 환경변수, 학습 데이터는 삭제하지 않습니다.

## 정상 로그
- `Health server listening on port 8080`
- `A100 V116.1 DEV S44.1 ... worker running...`
- `registered commands: 341`
- `Memory Containment safety audit: PASS`
- `Telegram single polling started`

## 실패 기준
`NameError: name 'Path' is not defined` 또는 수 초 간격의 `Mounting volume` 반복이 다시 보이면 배포를 중단하고 로그를 공유합니다.
