# S50.1 패치 설치 안내

1. ZIP을 해제합니다.
2. `main.py`를 기존 저장소의 동일 경로에 덮어씁니다.
3. 기존 `/data`, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. GitHub에 변경 파일을 반영한 뒤 Railway에서 재배포합니다.

## 배포 후 확인

```text
/version
/evidence
/releasegate
/releasegate detail
/errors
```

정상 기준:
- `/evidence`가 미지원 메시지 대신 Live Runtime Evidence 요약을 반환
- `/releasegate`가 대기 안내만 남기지 않고 최종 요약을 즉시 반환
- Registry 341/341 유지
- 신규 NameError/TypeError/KeyError/AttributeError 없음
