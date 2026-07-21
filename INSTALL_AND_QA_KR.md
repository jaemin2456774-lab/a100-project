# 설치 및 QA

1. ZIP의 `main.py`를 기존 Railway 애플리케이션에 교체합니다.
2. 기존 requirements와 volume을 유지한 채 재배포합니다.
3. 다음 순서로 확인합니다.

```text
/version
/buildinfo
/versionaudit
/commandcert
/commandcert
/commandmatrix
/commandmatrix
/trustgate
/trustgate
/profiling   또는 /performance
/errors
```

## 기대 결과
- Registry 341/341
- Architecture Guard PASS
- 두 번째 조회에서 Cache HIT
- Query render 시간이 첫 호출보다 감소
- Trust 조회 Ledger append NONE
- Historical new QA/BG/Unknown delta 0
- 성능 진단에서 P50/P95 및 budget 표시
