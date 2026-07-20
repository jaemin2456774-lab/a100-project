# S59.7.20 설치 및 검수

1. Railway 기존 코드와 데이터 볼륨을 백업합니다.
2. 패치의 `main.py`를 배포 대상에 적용합니다.
3. 기존 `/data` 및 Runtime/Learning 파일은 삭제하지 않습니다.
4. Railway 재배포 후 아래 순서로 확인합니다.

```
/version
/versionaudit
/papershadow
/papershadowstatus
/papershadowpositions
/papershadowperformance
/errors
```

## 기대값
- Version `S59.7.20`
- Registry `341/341`
- Version Audit `PASS`
- Shadow Worker `RUNNING`
- 최근 Market Scan 및 Shadow Capture 시간 표시
- Candidate 수와 필터 사유 표시
- 신규 Producer 오류 0건

첫 배포 직후에는 다음 Shadow capture까지 최대 약 120초가 필요할 수 있습니다.
