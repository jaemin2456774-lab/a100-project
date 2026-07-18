# A100 V116.1 DEV S44 설치 안내

이 패치는 V116.1 DEV 전용입니다. 인증 중인 V116.0 LTS Railway 서비스에는 적용하지 마십시오.

1. S43이 적용된 DEV 저장소 루트에 ZIP 내용을 덮어씁니다.
2. `/data`, 환경변수, 기존 학습/Outcome 데이터는 삭제하지 않습니다.
3. 기본 임계값은 Soft 760MB / Hard 860MB입니다.
4. Railway 메모리 한도에 맞춰 필요 시 환경변수로 낮춰 설정합니다.
   - `A100_S44_MEMORY_SOFT_MB=700`
   - `A100_S44_MEMORY_HARD_MB=820`
5. 배포 후 `/version`, `/god`, `/releasegate detail`, `/errors`를 확인합니다.
6. Memory 그래프가 계속 직선 상승하거나 컨테이너가 재시작되면 이 패치만으로 근본 누수가 해결된 것으로 판단하지 말고 추가 프로파일링이 필요합니다.
