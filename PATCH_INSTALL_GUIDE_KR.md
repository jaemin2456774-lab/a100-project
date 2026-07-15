# 설치 안내

1. ZIP을 해제합니다.
2. 저장소 루트의 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 영구 볼륨은 삭제하지 않습니다.
4. GitHub에 변경 파일만 업로드하고 Railway를 재배포합니다.

## 배포 후 확인
`/version` → `/releasegate` → `/versionaudit` → `/errors`

정상 기준: S2.17.12 표시, Scheduler samples 증가, Persist attempts/OK 증가, 1h samples가 0에서 증가.
