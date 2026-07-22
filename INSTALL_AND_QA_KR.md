# A100 V118.0 RC3.7 설치 및 QA

1. 패치의 `main.py`를 기존 프로젝트에 덮어씁니다.
2. Railway에서 재배포 또는 재시작합니다.
3. 아래 명령을 실행합니다.

```text
/version
/buildinfo
/versionaudit
/performance
/performancebudget
/perf
/errors
```

## 기대 결과
- 세 성능 명령이 같은 `A100 PERFORMANCE BUDGET · V118.0 RC3.7` 출력을 반환합니다.
- `/performancebudget`, `/perf`가 더 이상 지원하지 않는 명령으로 표시되지 않습니다.
- Registry는 341/341을 유지합니다.
- Architecture Guard와 Version Audit은 PASS여야 합니다.
