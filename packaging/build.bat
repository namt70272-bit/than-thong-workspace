@echo off
chcp 65001 >nul
title 🧿 Thần Thông — Build App
echo ====================================
echo   🧿 Thần Thông App Builder
echo ====================================
echo.

:: Check dependencies
echo [1/4] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Install Python 3.10+
    pause
    exit /b 1
)
echo ✅ Python found

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Some deps failed, continuing...
)

echo [3/4] Installing PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% neq 0 (
    echo ❌ PyInstaller install failed
    pause
    exit /b 1
)
echo ✅ PyInstaller ready

echo [4/4] Building app...
python build.py --onefile
if %ERRORLEVEL% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ====================================
echo   ✅ BUILD COMPLETE
echo ====================================
echo   Output: dist\than-thong.exe
echo   Size:   check above
echo ====================================
echo.
echo   Usage:
echo     than-thong.exe           — System tray app
echo     than-thong.exe console   — Interactive console
echo     than-thong.exe win-cleanup — Run cleanup
echo.
pause
