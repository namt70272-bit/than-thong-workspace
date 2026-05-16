@echo off
chcp 65001 >nul
title Gỡ ứng dụng - Uninstall Tools
echo ============================================
echo        GỠ ỨNG DỤNG HÀNG LOẠT
echo  [33m(Nhấn Ctrl+C để hủy bất kỳ lúc nào)[0m
echo ============================================
echo.

:: Request admin elevation
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [31m[!] Cần quyền Administrator![0m
    echo Click chuot phai -> Run as Administrator
    echo.
    pause
    exit /b 1
)

echo [36m[1/10] Dang go WinDirStat...[0m
start /wait msiexec /x {9D026C5A-F643-4F7E-97BF-0D973FA1D06A} /quiet /norestart
if %errorLevel% equ 0 (echo  [32mOK[0m) else (if %errorLevel% equ 1605 (echo  [33m(da go roi)[0m) else (echo  [31mLOI %errorLevel%[0m))

echo [36m[2/10] Dang go LiteManager Viewer...[0m
start /wait msiexec /x {5686E484-7136-4674-A4B2-508C7B26DCA4} /quiet /norestart
if %errorLevel% equ 0 (echo  [32mOK[0m) else (if %errorLevel% equ 1605 (echo  [33m(da go roi)[0m) else (echo  [31mLOI %errorLevel%[0m))

echo [36m[3/10] Dang go .NET Core 3.1 Runtime...[0m
start /wait msiexec /x {530DBE8F-D415-4661-9841-0C02A6A4CC50} /quiet /norestart
if %errorLevel% equ 0 (echo  [32mOK[0m) else (if %errorLevel% equ 1605 (echo  [33m(da go roi)[0m) else (echo  [31mLOI %errorLevel%[0m))

echo [36m[4/10] Dang go VLC media player...[0m
if exist "C:\Program Files\VideoLAN\VLC\uninstall.exe" (
    start /wait "" "C:\Program Files\VideoLAN\VLC\uninstall.exe" /S
    echo  [32mOK[0m
) else (echo  [33m(khong tim thay)[0m)

echo [36m[5/10] Dang go UltraUXThemePatcher...[0m
if exist "C:\Program Files (x86)\UltraUXThemePatcher\Uninstall.exe" (
    start /wait "" "C:\Program Files (x86)\UltraUXThemePatcher\Uninstall.exe" /S
    echo  [32mOK[0m
) else (echo  [33m(khong tim thay)[0m)

echo [36m[6/10] Dang go MEmu (Android emulator)...[0m
if exist "D:\Program Files\Microvirt\MEmu\uninstall\uninstall.exe" (
    start /wait "" "D:\Program Files\Microvirt\MEmu\uninstall\uninstall.exe" /S
    echo  [32mOK[0m
) else (
    if exist "D:\Program Files\Microvirt" (
        echo  [33m(Khong tim thay uninstaller, xoa thu muc...)[0m
        rmdir /s /q "D:\Program Files\Microvirt"
        echo  [32mOK (da xoa thu muc)[0m
    ) else (echo  [33m(khong tim thay)[0m)
)

echo [36m[7/10] Dang go Python 3.7 (8 components)...[0m
for %%c in (
    {C237EF2C-855C-4003-9442-12CEA8576DF6}
    {3AA7D71A-FE09-4269-B204-9B68EC6C77D0}
    {F88E9B2F-D249-4067-8DD7-D38D58CBF504}
    {347944F1-CE1B-4391-AB93-0CAFD0CCCC6B}
    {59D5D25E-5C3D-45FD-AA3D-73AFAB41BCBA}
    {04F5CDB6-698E-4B02-87AD-5C8353217917}
    {767A9C9C-AAB3-4364-A287-0BC6F4717658}
    {AB162684-2E4A-435C-9100-9E8454413464}
    {E6AF7FCC-01FD-4702-B569-485066BF85D3}
) do (
    start /wait msiexec /x %%c /quiet /norestart
)
echo  Python 3.7 da duoc xu ly.

echo [36m[8/10] Dang go NVIDIA CUDA Toolkit 13.2...[0m
:: Xoa thu muc CUDA truc tiep (nhanh gon nhat)
if exist "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2" (
    rmdir /s /q "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2"
    echo  [32mDa xoa CUDA Toolkit folder[0m
)
:: Xoa ca Component folder
if exist "C:\Program Files\NVIDIA GPU Computing Toolkit" (
    rmdir /s /q "C:\Program Files\NVIDIA GPU Computing Toolkit"
    echo  [32mDa xoa NVIDIA GPU Computing Toolkit folder[0m
)
:: Xoa Nsight
start /wait msiexec /x {F4FA3FDC-B834-42AF-AA28-DE8F193D0848} /quiet /norestart
start /wait msiexec /x {0A70A905-EF2F-4D33-8766-D910D47EB96F} /quiet /norestart
echo  DA XONG: CUDA Toolkit 13.2 + Nsight

echo [36m[9/10] Dang xoa NVIDIA cache...[0m
if exist "C:\ProgramData\NVIDIA Corporation\Downloader" (rmdir /s /q "C:\ProgramData\NVIDIA Corporation\Downloader" 2>nul & mkdir "C:\ProgramData\NVIDIA Corporation\Downloader" 2>nul)
if exist "C:\ProgramData\NVIDIA Corporation\Installer2" (rmdir /s /q "C:\ProgramData\NVIDIA Corporation\Installer2" 2>nul & mkdir "C:\ProgramData\NVIDIA Corporation\Installer2" 2>nul)
if exist "C:\ProgramData\NVIDIA Corporation\NVSMI" (rmdir /s /q "C:\ProgramData\NVIDIA Corporation\NVSMI" 2>nul & mkdir "C:\ProgramData\NVIDIA Corporation\NVSMI" 2>nul)
if exist "C:\ProgramData\NVIDIA Corporation\InstallCache" (rmdir /s /q "C:\ProgramData\NVIDIA Corporation\InstallCache" 2>nul & mkdir "C:\ProgramData\NVIDIA Corporation\InstallCache" 2>nul)
echo  [32mCache da duoc don sach[0m

echo [36m[10/10] Don Registry entries (CUDA)...[0m
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDARuntimes_13.2" /f 2>nul
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADevelopment_13.2" /f 2>nul
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADocument_13.2" /f 2>nul
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDAToolkit_13.2" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDARuntimes_13.2" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADevelopment_13.2" /f 2>nul
echo  [32mRegistry da don[0m

echo.
echo ============================================
echo         [32mHOAN THANH![0m
echo ============================================
echo.
echo Tong tien: ~15-20 GB duoc giai phong
echo.
echo Kiem tra trong: Settings ^> Apps ^> Installed apps
echo.
pause
