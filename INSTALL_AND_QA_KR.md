# A100 V118.0 RC3 설치 및 검수

1. 기존 프로젝트의 `main.py`를 이 패치의 파일로 덮어씁니다.
2. Railway에 배포 후 재시작 로그에서 V118.0 RC3 Build ID와 Registry 341을 확인합니다.
3. 아래 명령을 순서대로 실행합니다.

```text
/version
/buildinfo
/versionaudit
/commandcert
/commandcert
/commandmatrix
/commandmatrix
/trustgate
/trustgate
/intelligencescore
/performance
```

성능 최종 판정에는 기본 5개 샘플이 필요합니다. 동일 명령을 60초 TTL 안에서 총 5회 실행한 후 `/performance`를 다시 확인합니다.

## 필수 확인

- `/versionaudit` Result PASS
- `QA Provenance Isolated` PASS
- Background / Unknown 0
- Registry 341/341
- 두 번째 `/commandmatrix`, `/trustgate`, `/commandcert`에서 Cache HIT
- `/performance`에서 Samples, Hits/Misses 표시
- 샘플 0건이 PASS로 표시되지 않음
- Live Trading OFF
