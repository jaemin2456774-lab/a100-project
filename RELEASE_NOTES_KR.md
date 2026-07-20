# A100 V116.2 RC1.4
## Authoritative Route Lock & State Signature Cache

- 부팅 중 legacy route installer 실행 후 RC1.4 핵심 route를 다시 고정합니다.
- /buildinfo, /routeraudit, /runtimehealth, /versionaudit, /papershadow, /coverageplan의 표시 Identity를 RC1.4로 통일합니다.
- /papershadowperformance 캐시를 시간 TTL 방식에서 durable state 파일 mtime/size 서명 방식으로 변경합니다.
- 상태 파일이 바뀌지 않은 연속 호출은 JSON 전체 재읽기 없이 캐시를 반환합니다.
- Registry 341/341, Runtime First, Strict Read Only, Live OFF를 유지합니다.
- Entry Gate, Threshold, TP/SL, 전략 및 Learning 저장 로직은 변경하지 않습니다.
