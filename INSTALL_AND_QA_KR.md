# 설치 및 Railway QA

1. 기존 데이터 볼륨을 유지한 채 `main.py`를 교체합니다.
2. Railway 재배포 후 아래 순서로 실행합니다.

```text
/version
/versionaudit
/papershadow
/errors
```

## 기대 결과
- V116.2 RC1
- Registry 341/341
- Version Audit PASS
- Shadow Current Scan / Active Queue 분리 출력
- Consistency 항목 표시
- System Error 0

기존 Runtime/Learning 데이터는 삭제하지 않습니다.
