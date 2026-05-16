@echo off
echo === Installing GitHub Actions Runner Service ===
cd /d "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\runner"
echo Configuring runner as service...
.\config.cmd --url "https://github.com/namt70272-bit/than-thong-workspace" --token "CBECPJDXUJHKKZ3JZNTR4ZDKBBVU2" --runasservice --replace
echo Starting service...
.\svc.cmd start
echo === Done! Service should be running ===
sc query GitHubActionsRunner | findstr STATE
pause
