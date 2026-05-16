@echo off
echo ==================================================
echo   Cai dat GitHub Actions Runner Service
echo   Repo: than-thong-workspace
echo ==================================================
echo.

cd /d "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\runner"

echo [1/3] Dang ky runner...
.\config.cmd --url "https://github.com/namt70272-bit/than-thong-workspace" --token "CBECPJDXUJHKKZ3JZNTR4ZDKBBVU2" --runasservice --replace

echo.
echo [2/3] Cai dat service...
Runner.Listener.exe install --runas "NT AUTHORITY\SYSTEM"

echo.
echo [3/3] Khoi dong service...
net start GitHubActionsRunner

echo.
sc query GitHubActionsRunner | findstr STATE
echo.
echo ==================================================
echo   Hoan tat! Service dang chay.
echo ==================================================
pause
