# GitHub 기존 파일 전체 삭제 후 교체

## 모바일 웹 방식

GitHub 웹 업로드는 한 번에 100개 제한이 있으나 이 릴리스는 그보다 적은 파일로 구성되어 있습니다.

1. 저장소에서 기존 파일을 삭제합니다.
2. 삭제 커밋 메시지: `Remove legacy release files`
3. 이 ZIP을 휴대폰에서 압축 해제합니다.
4. `A100_V94_1_GITHUB_CLEAN_RELEASE` 폴더 안의 파일과 폴더를 선택합니다.
5. 저장소 루트에 업로드합니다. 상위 폴더 자체를 한 단계 더 중첩하지 않습니다.
6. 커밋 메시지: `Deploy A100 V94.1 clean release`

## 권장 Git 명령 방식

```bash
git clone <YOUR_REPOSITORY>
cd a100-project
git rm -r .
# 압축을 푼 릴리스의 내부 파일을 이 폴더로 복사
git add -A
git commit -m "Deploy A100 V94.1 clean release"
git push
```

## 절대 삭제하면 안 되는 운영 데이터

GitHub 파일 삭제는 Railway 영구 볼륨을 삭제하는 작업과 다릅니다. Railway에서 다음 항목은 유지해야 합니다.

- 환경변수와 Telegram 토큰
- 영구 볼륨
- `a100_v91_paper_state.json`

상태 JSON을 GitHub에 새로 업로드하지 마십시오. 빈 상태 파일이 운영 데이터를 덮어쓸 수 있습니다.
