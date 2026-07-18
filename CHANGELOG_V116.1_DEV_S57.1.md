# A100 V116.1 DEV S57.1

## Application Callback Recovery · Virtual Route Identity Hotfix

- 실제 Telegram Application callback을 최종 `v90_1_dispatch`로 고정
- 과거 dispatcher callback이 캡처되어도 `Registry.get()`에서 호환 명령을 해석하는 Virtual Registry 추가
- `/buildinfo`, `/connectivity`, `/verifyall`, `/routeraudit`를 Registry 슬롯 증가 없이 제공
- Registry 길이 341 유지
- `/status`, `/runtimehealth`의 LTS 버전 문자열을 S57.1 Build Identity로 정규화
- `/version`, `/status`, `/runtimehealth` 단일 Build ID 적용
- Application callback 이름과 object ID 진단 추가
- Synthetic completion OFF, Gate 계산식 변경 없음, Live OFF 유지
