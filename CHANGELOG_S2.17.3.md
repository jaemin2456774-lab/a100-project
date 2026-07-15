# A100 V116.0 LTS-S2.17.3
## Non-Blocking Release Gate & Snapshot Cache Patch

- `/releasegate`를 Dispatcher 비차단 방식으로 변경했습니다.
- 명령 요청 경로에서 전체 Production Engine을 재계산하지 않습니다.
- 5분 TTL의 Immutable Certification Snapshot Cache를 재사용합니다.
- 즉시 접수 메시지를 보낸 뒤 별도 Background Task가 최종 결과를 전송합니다.
- 최종 전송은 30초 제한과 예외 기록을 적용합니다.
- Mandatory Gate별 Primary/Secondary Gap과 정보성 Velocity ETA를 추가했습니다.
- Outcome Quality 진단 블록을 추가했습니다.
- Mandatory Gate의 실제 판정 기준과 목표값은 변경하지 않았습니다.
- Schema 1, Paper 20, Shadow 60, Live OFF 및 Registry 341을 유지합니다.
