# A100 V118.0 RC3.5 릴리스 노트

Build ID: `V118.0-RC3.5-20260722-RECOVERY-INTERNAL-PROFILING-SEMANTIC-WARM-CACHE-01`

## 변경 사항

- Recovery 내부를 단계별로 실측합니다.
  - recovery_ledger_load
  - recovery_ledger_migrate
  - recovery_ledger_refresh
  - recovery_replay_verify
  - recovery_matrix_refresh
- 부팅 시 핵심 read-only 출력 4종을 미리 렌더링합니다.
  - /commandcert
  - /commandmatrix
  - /trustgate
  - /intelligencescore
- /commandcert는 semantic projection hash가 유지되는 동안 300초 TTL을 사용합니다.
- 다른 Render Cache는 기존 60초 TTL을 유지합니다.
- Warmup은 성능 샘플이나 Ledger event를 생성하지 않습니다.
- Registry 341/341, Strict Read Only, Live Trading OFF를 유지합니다.

## 기대 결과

- 배포 직후 핵심 명령 첫 호출부터 Cache HIT 가능
- /commandcert의 불필요한 60초 EXPIRED 감소
- 약 10초 Recovery 병목의 실제 하위 단계 확인
