@echo off
REM rollback.cmd — Rollback workspace về commit ổn định
REM Usage: rollback [commit-hash] hoặc rollback (về commit cuối cùng trên master)

setlocal
cd /d "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"

if "%~1"=="" (
    echo Rollback ve commit cuoi cung...
    git reset --hard HEAD~1
) else (
    echo Rollback ve commit: %~1
    git reset --hard %~1
)

echo.
echo === Workspace rollback hoan tat ===
git log --oneline -3
echo.
echo Chay 'git push --force-with-lease' de cap nhat GitHub
echo neu can dong bo remote.
echo.
pause
