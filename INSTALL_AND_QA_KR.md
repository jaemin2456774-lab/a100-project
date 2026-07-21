# 설치 및 QA

기존 main.py를 패치의 main.py로 교체하고 기존 requirements 및 volume을 유지해 재배포합니다.

검증 순서:

```
/version
/buildinfo
/commandcert
/commandcert status
/commandmatrix
/commandcert batch 1 run
/commandcert status
/versionaudit
/trustgate
/errors
```

기대값:
- 일반 조회 render 시간이 짧게 표시
- 반복 조회 시 Projection hash와 PASS 수가 동일
- 일반 timeout 6초, slow timeout 10초
- 느린 명령이 있어도 Batch가 다음 명령으로 진행
- Slow queue 수가 status에 표시
- Counter 및 Historical reconciliation PASS
