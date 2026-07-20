# Railway 설치 및 QA

1. 패치의 `main.py`를 저장소의 기존 `main.py`에 덮어씁니다.
2. Railway에서 새 배포를 실행합니다.
3. `/data` 볼륨과 환경변수는 그대로 유지합니다.

## 검증 순서
```text
/version
/buildinfo
/runtimehealth
/versionaudit
/commandcert
/commandcert full
/commandcert batch 1
/commandcert report
/commandmatrix
/papershadow
/errors
```

## 기대값
- Registry 341/341
- Version Audit PASS
- Total 341
- 등록만 된 미실행 명령은 PARTIAL
- 끊어진 Handler/Route만 FAILED
- `/papershadow` 점수/기준/Gap이 소수점 둘째 자리로 표시
- Gate/Threshold/Live mutation NONE
