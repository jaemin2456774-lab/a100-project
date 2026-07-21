# 설치 및 QA

Railway에 main.py를 배포한 뒤 실행:

/version
/buildinfo
/versionaudit
/versionaudit
/commandcert batch 1 run
/commandcert status
/versionaudit
/commandcert
/commandmatrix
/errors

기대값:
- Mutation Firewall Active
- Batch historical reconciliation PASS
- Mutation blocked 0
- Upsert PASS
- Post-firewall Delta 0/0/0
- 두 번째 versionaudit PASS
