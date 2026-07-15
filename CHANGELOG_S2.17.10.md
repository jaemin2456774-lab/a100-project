# A100 V116.0 LTS-S2.17.10
## Persisted Snapshot Restore · Gate Evidence · Runtime Metrics

- Railway 재시작 뒤 `/data`의 마지막 정상 인증 Snapshot을 검증 후 즉시 복원합니다.
- 정책 fingerprint가 다르거나 Snapshot이 손상된 경우 복원하지 않고 기존 안전한 백그라운드 빌드 경로를 사용합니다.
- Snapshot 저장은 임시 파일 작성 후 `os.replace()`로 원자적 교체합니다.
- Cold-start 복원 시간, 복원 성공/실패, Snapshot 저장 횟수와 실패 횟수를 출력합니다.
- `/releasegate`에 Gate별 권위 있는 Evidence 우선순위를 추가하되 점수나 Mandatory Gate 기준은 변경하지 않습니다.
- `/releasegate`와 `/versionaudit`의 비차단 처리, TTL Cache, Single-Flight, Proactive Refresh, Stale Fallback을 유지합니다.
- Schema 1, Paper 20, Shadow 60, Live Trading OFF, Registry 341 정책을 유지합니다.
