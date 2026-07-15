# S2.17.6 패치 설치 안내

1. ZIP을 해제합니다.
2. GitHub 저장소 루트의 기존 `main.py`를 패치의 `main.py`로 덮어씁니다.
3. 기존 `/data`, 환경변수, Railway Volume은 삭제하지 않습니다.
4. GitHub에 커밋한 뒤 Railway 재배포를 확인합니다.

## 배포 후 확인

```text
/version
/versionaudit
/releasegate
/errors
```

정상 기준:
- `/version`에 S2.17.6 표시
- `/versionaudit`의 `PREFLIGHT SUMMARY PASS`, Failures 0
- 각 검사 항목 PASS/WARN/FAIL 상세 표시
- `/versionaudit`와 `/releasegate` Snapshot ID/Hash 일치
- 새 120초 timeout 오류 없음
