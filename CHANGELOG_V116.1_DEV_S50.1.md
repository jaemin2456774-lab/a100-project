# A100 V116.1 DEV S50.1

## Evidence Command Compatibility & ReleaseGate Immediate Result Hotfix

- `/evidence` 명령을 Registry 341/341을 변경하지 않는 dispatcher 호환 경로로 복구했습니다.
- `/evidence`는 Live Runtime의 refresh, change, sample, 72H coverage, gate consistency를 Strict Read Only로 표시합니다.
- `/releasegate`가 레거시 대기 안내만 남기는 경로를 우회하고 현재 S43 certification diagnostics 결과를 즉시 반환하도록 수정했습니다.
- `/releasegate detail` 상세 모드를 유지합니다.
- ReleaseGate 렌더러 예외 시에도 읽기 전용 fallback 결과를 반환하며 Gate 상태를 변경하지 않습니다.
- Registry 341/341, Schema 1, Paper 20, Shadow 60, Live OFF 유지.
- Synthetic Evidence/PASS, Gate recomputation, threshold relaxation, state mutation 없음.
