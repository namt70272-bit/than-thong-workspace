@ECHO off
SETLOCAL
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ttt.ps1" %*
EXIT /B %ERRORLEVEL%
