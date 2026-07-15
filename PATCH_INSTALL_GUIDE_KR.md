# S2.17.5 패치 설치

1. ZIP 압축을 풉니다.
2. 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. 기존 `/data` 볼륨과 환경변수는 변경하지 않습니다.
4. GitHub에 커밋 후 Railway 재배포합니다.

## 배포 후 확인
```text
/version
/versionaudit
/releasegate
/errors
```

`/versionaudit`는 즉시 접수 메시지를 보내고 최종 결과를 별도 메시지로 전송해야 합니다. 기존 timeout 기록은 이력으로 남을 수 있으나 새 timeout이 추가되면 안 됩니다.
