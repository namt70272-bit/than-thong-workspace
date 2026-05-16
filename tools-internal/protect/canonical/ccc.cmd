@ECHO off
SETLOCAL
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ccc.ps1" %*
EXIT /B %ERRORLEVEL%
