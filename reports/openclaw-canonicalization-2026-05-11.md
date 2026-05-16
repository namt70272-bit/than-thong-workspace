# OpenClaw canonicalization note — 2026-05-11 00:25 GMT+7

## Decision
- Canonical runtime/data root: `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw`
- Canonical workspace: `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`
- No package update performed.

## Backup created
- `E:\KY-DATA\OpenClaw\backups\openclaw-pre-cleanup-20260511-001735`
  - `C-runtime`
  - `E-runtime`
  - `docs`

## Verification
- Active E config already uses `runtime.acp.cwd = ${OPENCLAW_WORKSPACE}`.
- `C:\Users\ACER\.openclaw\gateway.cmd` already launches Gateway with:
  - `OPENCLAW_HOME=E:\KY-DATA\OpenClaw\runtime-mirror`
  - `OPENCLAW_WORKSPACE=E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`
  - code path `E:\KY-DATA\OpenClaw\code-mirror\npm\node_modules\openclaw\dist\index.js`
- `gateway-e.cmd` and `gateway-e-native.cmd` also point to E.

## Scheduled Task status
- Windows Scheduled Task `OpenClaw Gateway` now points directly to `E:\KY-DATA\OpenClaw\gateway-e-native.cmd`.
- This removes the last important operational dependency on the C launcher path.

## Recommended next cleanup
1. Archive old `C:\Users\ACER\.openclaw` legacy state instead of deleting immediately.
2. Optionally run one controlled Gateway restart later to confirm the task/launcher path end-to-end.
