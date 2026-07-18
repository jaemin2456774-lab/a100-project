# A100 V116.1 DEV S57.7 Railway Patch Install Guide

1. Back up the current repository and Railway volume.
2. Extract this patch over the repository root.
3. Commit and push only the changed files.
4. Deploy through Railway.
5. Confirm startup logs contain:
   - `V116.1-DEV-S57.7 worker running...`
   - `BUILD_ID=S57.7-20260719-ENGINE-E2E-SOURCE-TRUTH-01`
   - `engine E2E source truth: PIPELINE RUNTIME`
6. Run:
   - `/version`
   - `/buildinfo`
   - `/routeraudit`
   - `/versionaudit`
   - `/engineaudit`
   - `/pipelineaudit`
   - `/verifyall`
   - `/verifyall detail`
   - `/errors`

Approval requires Registry 341/341, Version Audit PASS, Engine E2E PASS,
VerifyAll PASS, Same-ID Trace PASS, Revision Integrity PASS, and Errors 0.
