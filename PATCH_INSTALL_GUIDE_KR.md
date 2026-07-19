# S59.7.12 Railway 패치 설치 안내

1. ZIP의 `main.py`를 현재 저장소의 `main.py`에 덮어씁니다.
2. 기존 `/data`, 환경변수 및 학습 데이터는 삭제하지 않습니다.
3. Railway에서 새 배포를 실행합니다.
4. 배포 후 다음 명령을 순서대로 확인합니다.

```
/version
/versionaudit
/strategyperformance
/strategytrust
/memoryhealth
/championstability
/errors
```

정상 기대값: Registry 341/341, Version Audit PASS, 각 적응형 출력에 S59.7.12와 History 지점 수 표시, 신규 오류 없음.
