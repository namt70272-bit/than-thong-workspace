# ccc/ttt guard

Canonical copies and hardening flow for `ccc` and `ttt` live on **E:**.

## Live location
- `E:\KY-DATA\OpenClaw\bin\ccc.ps1`
- `E:\KY-DATA\OpenClaw\bin\ccc.cmd`
- `E:\KY-DATA\OpenClaw\bin\ttt.ps1`
- `E:\KY-DATA\OpenClaw\bin\ttt.cmd`

## Canonical location
- `tools-internal\protect\canonical\ccc.ps1`
- `tools-internal\protect\canonical\ccc.cmd`
- `tools-internal\protect\canonical\ttt.ps1`
- `tools-internal\protect\canonical\ttt.cmd`

## Guard
- `tools-internal\protect\ccc-ttt-guard.ps1`

## Purpose
- restore missing or drifted shims from canonical copies
- keep active shims on **E:**
- apply hard lock with read-only + ACL deny write/delete on live files

## Commands
```powershell
powershell -ExecutionPolicy Bypass -File tools-internal\protect\ccc-ttt-guard.ps1 status
powershell -ExecutionPolicy Bypass -File tools-internal\protect\ccc-ttt-guard.ps1 enforce
powershell -ExecutionPolicy Bypass -File tools-internal\protect\ccc-ttt-guard.ps1 hard-unlock
powershell -ExecutionPolicy Bypass -File tools-internal\protect\ccc-ttt-guard.ps1 repair
```

## Notes
- prepend `E:\KY-DATA\OpenClaw\bin` into user PATH so `ccc/ttt` resolve from E first
- legacy copies under `%APPDATA%\npm` can remain as fallback, but active resolution should come from E
