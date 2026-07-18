# S49.1 Railway 증분 패치 설치 안내

1. 기존 S49 배포 파일 위에 패치의 `main.py`를 덮어씁니다.
2. `/data` 볼륨, 환경변수, 학습 데이터, 설정 파일은 삭제하거나 초기화하지 않습니다.
3. GitHub에 변경 파일을 반영한 뒤 Railway에서 새 배포를 실행합니다.
4. 시작 로그에서 아래 항목을 확인합니다.

```text
A100 V116.1 DEV S49.1 worker running...
A100 V116.1 DEV S49.1 Explainable AI schema compatibility audit: PASS
A100 V116.1 DEV S49.1 Explainable AI 2.1 schema compatibility: ACTIVE
A100 V116.1 DEV S49.1 synthetic evidence/pass: DISABLED
A100 V116.1 DEV S49.1 live trading: OFF
```

5. 아래 오류가 배포 시각 이후 재발하지 않아야 합니다.

```text
TypeError: float() argument must be a string or a real number, not 'dict'
```

6. 검증 명령:

```text
/version
/runtimehealth
/ultimate detail
/god
/errors
```
