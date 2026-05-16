# C legacy inventory — 2026-05-11 01:10 GMT+7

## Current state
`C:\Users\ACER\.openclaw` is already very small and no longer appears to hold active runtime data.

## Remaining items
- `gateway.cmd` — legacy launcher stub
- `openclaw.json`
- `openclaw.json.bak`
- `openclaw.json.bak.1`
- `openclaw.json.last-good`
- `.env`
- `exec-approvals.json`
- `update-check.json`
- `package.json`
- `package-lock.json`
- `pnpm-lock.yaml`
- `workspace\` — empty at time of check

## Assessment
- Active Gateway task now points directly to `E:\KY-DATA\OpenClaw\gateway-e-native.cmd`.
- Active runtime/workspace/config are on E.
- No meaningful user/workspace payload remains under the C runtime root.

## Safe next move
After one controlled restart validates clean boot from E, archive the remaining `C:\Users\ACER\.openclaw` stub files into backup storage instead of deleting immediately.
