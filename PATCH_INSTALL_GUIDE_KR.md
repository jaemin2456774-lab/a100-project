# S2.17.10 패치 설치

1. ZIP을 해제합니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. `/data` 또는 `A100_DATA_DIR`가 Railway 영구 볼륨인지 확인합니다.
4. GitHub에 커밋한 뒤 Railway 재배포를 확인합니다.

## 배포 후 검증

```text
/version
/releasegate
/versionaudit
/errors
```

두 번째 재배포부터 `Persistent Restore 1 hit` 또는 `Restore Status Persistent snapshot restored`가 표시되면 정상입니다. 최초 배포에서는 저장 파일이 없어 miss가 정상일 수 있습니다.
