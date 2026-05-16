#requires -Version 5.1

# Tự động elevate lên Administrator nếu chưa có quyền
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[!] Dang xin quyen Administrator..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "           GO UNG DUNG HANG LOAT" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$success = 0; $fail = 0; $skip = 0

function Write-Result {
    param([string]$Label, [int]$ExitCode)
    if ($ExitCode -eq 0) { Write-Host "  [$Label] OK" -ForegroundColor Green; $script:success++ }
    elseif ($ExitCode -eq 1605) { Write-Host "  [$Label] (da go roi)" -ForegroundColor Gray; $script:skip++ }
    else { Write-Host "  [$Label] LOI $ExitCode" -ForegroundColor Red; $script:fail++ }
}

# --- 1. WinDirStat ---
Write-Host "[1/10] WinDirStat..." -ForegroundColor Cyan
$p = Start-Process msiexec -ArgumentList "/x {9D026C5A-F643-4F7E-97BF-0D973FA1D06A} /quiet /norestart" -Wait -NoNewWindow -PassThru
Write-Result "WinDirStat" $p.ExitCode

# --- 2. LiteManager Pro Viewer ---
Write-Host "[2/10] LiteManager Viewer..." -ForegroundColor Cyan
$p = Start-Process msiexec -ArgumentList "/x {5686E484-7136-4674-A4B2-508C7B26DCA4} /quiet /norestart" -Wait -NoNewWindow -PassThru
Write-Result "LiteManager" $p.ExitCode

# --- 3. .NET Core 3.1 Runtime ---
Write-Host "[3/10] .NET Core 3.1 Runtime..." -ForegroundColor Cyan
$p = Start-Process msiexec -ArgumentList "/x {530DBE8F-D415-4661-9841-0C02A6A4CC50} /quiet /norestart" -Wait -NoNewWindow -PassThru
Write-Result ".NET Core 3.1" $p.ExitCode

# --- 4. VLC media player ---
Write-Host "[4/10] VLC media player..." -ForegroundColor Cyan
$vlcUninstall = "C:\Program Files\VideoLAN\VLC\uninstall.exe"
if (Test-Path $vlcUninstall) {
    $p = Start-Process $vlcUninstall -ArgumentList "/S" -Wait -NoNewWindow -PassThru
    Write-Result "VLC" $p.ExitCode
} else { Write-Host "  [VLC] khong tim thay" -ForegroundColor Gray; $skip++ }

# --- 5. UltraUXThemePatcher ---
Write-Host "[5/10] UltraUXThemePatcher..." -ForegroundColor Cyan
$uxtUninstall = "C:\Program Files (x86)\UltraUXThemePatcher\Uninstall.exe"
if (Test-Path $uxtUninstall) {
    $p = Start-Process $uxtUninstall -ArgumentList "/S" -Wait -NoNewWindow -PassThru
    Write-Result "UltraUXThemePatcher" $p.ExitCode
} else { Write-Host "  [UltraUX] khong tim thay" -ForegroundColor Gray; $skip++ }

# --- 6. MEmu Android Emulator ---
Write-Host "[6/10] MEmu (Android emulator)..." -ForegroundColor Cyan
$memuPaths = @(
    "D:\Program Files\Microvirt\MEmu\uninstall\uninstall.exe",
    "D:\Program Files\Microvirt\uninstall\uninstall.exe"
)
$found = $false
foreach ($path in $memuPaths) {
    if (Test-Path $path) { $memuUninstall = $path; $found = $true; break }
}
if ($found) {
    $p = Start-Process $memuUninstall -ArgumentList "/S" -Wait -NoNewWindow -PassThru
    Write-Result "MEmu" $p.ExitCode
} else {
    Write-Host "  [MEmu] khong tim thay uninstaller, xoa thu muc..." -ForegroundColor Yellow
    $microvirtDir = "D:\Program Files\Microvirt"
    if (Test-Path $microvirtDir) {
        try { Remove-Item $microvirtDir -Recurse -Force; Write-Host "  [MEmu] da xoa thu muc" -ForegroundColor Green; $success++ }
        catch { Write-Host "  [MEmu] khong the xoa thu muc: $_" -ForegroundColor Red; $fail++ }
    } else { Write-Host "  [MEmu] khong tim thay" -ForegroundColor Gray; $skip++ }
}

# --- 7. Python 3.7 (all sub-components) ---
Write-Host "[7/10] Python 3.7..." -ForegroundColor Cyan
$py37Codes = @(
    @{Code="{C237EF2C-855C-4003-9442-12CEA8576DF6}"; Name="Core Interpreter"}
    @{Code="{3AA7D71A-FE09-4269-B204-9B68EC6C77D0}"; Name="Development Libs"}
    @{Code="{F88E9B2F-D249-4067-8DD7-D38D58CBF504}"; Name="Documentation"}
    @{Code="{347944F1-CE1B-4391-AB93-0CAFD0CCCC6B}"; Name="Executables"}
    @{Code="{59D5D25E-5C3D-45FD-AA3D-73AFAB41BCBA}"; Name="pip Bootstrap"}
    @{Code="{04F5CDB6-698E-4B02-87AD-5C8353217917}"; Name="Standard Library"}
    @{Code="{767A9C9C-AAB3-4364-A287-0BC6F4717658}"; Name="Tcl/Tk Support"}
    @{Code="{AB162684-2E4A-435C-9100-9E8454413464}"; Name="Test Suite"}
    @{Code="{E6AF7FCC-01FD-4702-B569-485066BF85D3}"; Name="Utility Scripts"}
)
foreach ($item in $py37Codes) {
    $p = Start-Process msiexec -ArgumentList "/x $($item.Code) /quiet /norestart" -Wait -NoNewWindow -PassThru
    Write-Result "Python37 - $($item.Name)" $p.ExitCode
}

# --- 8. NVIDIA CUDA Toolkit 13.2 ---
Write-Host "[8/10] NVIDIA CUDA Toolkit 13.2..." -ForegroundColor Cyan
$cudaDir = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2"
if (Test-Path $cudaDir) {
    try {
        Remove-Item $cudaDir -Recurse -Force
        Write-Host "  [CUDA] da xoa: $cudaDir" -ForegroundColor Green; $success++
    } catch { Write-Host "  [CUDA] loi xoa folder: $_" -ForegroundColor Red; $fail++ }
} else { Write-Host "  [CUDA] khong tim thay folder" -ForegroundColor Gray; $skip++ }

# Xoa toan bo NVIDIA GPU Computing Toolkit folder
$cudaParent = "C:\Program Files\NVIDIA GPU Computing Toolkit"
if (Test-Path $cudaParent) {
    try { Remove-Item $cudaParent -Recurse -Force; Write-Host "  [CUDA] da xoa parent folder" -ForegroundColor Green }
    catch { }
}

# Xoa NVIDIA Nsight Compute + Systems
Write-Host "  --> NVIDIA Nsight..."
$nsightCodes = @(
    @{Code="{F4FA3FDC-B834-42AF-AA28-DE8F193D0848}"; Name="Nsight Compute 2026.1.1"}
    @{Code="{0A70A905-EF2F-4D33-8766-D910D47EB96F}"; Name="Nsight Systems 2025.6.3"}
)
foreach ($item in $nsightCodes) {
    $p = Start-Process msiexec -ArgumentList "/x $($item.Code) /quiet /norestart" -Wait -NoNewWindow -PassThru
    Write-Result "$($item.Name)" $p.ExitCode
}

# Xoa registry entries CUDA
Write-Host "  --> Don registry CUDA entries..."
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDARuntimes_13.2" /f 2>$null
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADevelopment_13.2" /f 2>$null
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADocument_13.2" /f 2>$null
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDAToolkit_13.2" /f 2>$null
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDARuntimes_13.2" /f 2>$null
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_CUDADevelopment_13.2" /f 2>$null
Write-Host "  [CUDA] da don registry" -ForegroundColor Green

# --- 9. NVIDIA driver cache (ProgramData) ---
Write-Host "[9/10] NVIDIA driver cache..." -ForegroundColor Cyan
$cacheDirs = @(
    "C:\ProgramData\NVIDIA Corporation\Downloader",
    "C:\ProgramData\NVIDIA Corporation\Installer2",
    "C:\ProgramData\NVIDIA Corporation\NVSMI",
    "C:\ProgramData\NVIDIA Corporation\InstallCache"
)
foreach ($dir in $cacheDirs) {
    if (Test-Path $dir) {
        try {
            # Xoa noi dung ben trong, giu lai thu muc goc de tranh loi
            Get-ChildItem $dir -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  [Cache] da don: $dir" -ForegroundColor Green; $success++
        } catch { Write-Host "  [Cache] skip: $dir (dang dung)" -ForegroundColor Yellow; $skip++ }
    } else { Write-Host "  [Cache] khong co: $dir" -ForegroundColor Gray; $skip++ }
}

# --- 10. Xoa file temp cua cac app vua go ---
Write-Host "[10/10] Don dep temp + cache..." -ForegroundColor Cyan
$tempClean = @(
    "$env:LOCALAPPDATA\Temp",
    "$env:LOCALAPPDATA\VLC",
    "$env:LOCALAPPDATA\Microvirt",
    "$env:LOCALAPPDATA\MEmu",
    "$env:APPDATA\VLC",
    "$env:APPDATA\Microvirt",
    "$env:APPDATA\MEmu"
)
foreach ($dir in $tempClean) {
    if (Test-Path $dir) {
        try { Remove-Item "$dir\*" -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "  [Temp] don: $dir" -ForegroundColor Green }
        catch { }
    }
}
Write-Host "  [Temp] da don" -ForegroundColor Green

# --- KET QUA ---
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "            KET QUA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Thanh cong: $success" -ForegroundColor Green
Write-Host "  Da go truoc: $skip" -ForegroundColor Yellow
Write-Host "  That bai: $fail" -ForegroundColor Red
$totalGB = "~15-20 GB"
Write-Host "  Uoc tinh giai phong: $totalGB" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Kiem tra trong: Settings > Apps > Installed apps" -ForegroundColor Gray
Write-Host ""
pause
