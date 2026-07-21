# 설치 및 QA · V118.0 RC3.1

기존 프로젝트에 `main.py`를 덮어쓰고 Railway에서 재배포합니다. 데이터 볼륨과 환경변수는 변경하지 않습니다.

## 시작 로그 필수 확인
```text
A100 V118.0 RC3.1 runtime identity: CURRENT
A100 V118 architecture guard: PASS registry=341
```

## 텔레그램 검수
```text
/version
/buildinfo
/versionaudit
/performance
/errors
```

`/buildinfo`에서 Registry 341/341, Architecture Guard PASS를 확인합니다.
