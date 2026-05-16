#!/usr/bin/env pwsh
# GPU Monitor Script — Cảnh báo khi VRAM quá tải
# Chạy trong cron gateway-watchdog

$ErrorActionPreference = "Continue"
$warnPct = 80       # Cảnh báo khi VRAM > 80%
$criticalPct = 92   # Critical khi VRAM > 92%
$logDir = "E:\KY-DATA\OpenClaw\logs"
$logFile = Join-Path $logDir "gpu-monitor.log"
$stateFile = Join-Path $logDir "gpu-monitor-state.json"

# Tạo log dir nếu chưa có
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

# Lấy GPU info
try {
    $gpuInfo = nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader -l 1 2>$null
    if (-not $gpuInfo) {
        Write-Error "[WARN] nvidia-smi returned no output"
        exit 0
    }
    
    $parts = $gpuInfo[0] -split ', ' | ForEach-Object { $_.Trim() }
    $name = $parts[0]
    $util = [int]($parts[1] -replace ' %','')
    $memUsed = [int]($parts[2] -replace ' MiB','')
    $memTotal = [int]($parts[3] -replace ' MiB','')
    $temp = [int]($parts[4] -replace ' C','')
    $memPct = [math]::Round(($memUsed / $memTotal) * 100, 1)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "$timestamp | GPU:$name | VRAM:${memUsed}/${memTotal}MiB (${memPct}%) | Util:${util}% | Temp:${temp}C"
    
    # Ghi log
    Add-Content -Path $logFile -Value $logLine
    
    # Kiểm tra ngưỡng
    if ($memPct -ge $criticalPct) {
        Write-Host "[CRITICAL] VRAM ${memPct}% — $($memUsed)/$($memTotal)MiB"
        Write-Host "→ Đóng bớt ComfyUI hoặc Ollama model!"
    } elseif ($memPct -ge $warnPct) {
        Write-Host "[WARN] VRAM ${memPct}% — $($memUsed)/$($memTotal)MiB"
    } else {
        Write-Host "[OK] VRAM ${memPct}% — $($memUsed)/$($memTotal)MiB"
    }
    
    # Check conflicting processes
    $ollamaVRAM = 0; $comfyVRAM = 0
    $ollamaProc = Get-Process -Name "ollama*" -ErrorAction SilentlyContinue
    $comfyProc = Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "ComfyUI|comfy" 2>$null }
    
    if ($ollamaProc -and $comfyProc -and $memPct -ge 70) {
        Write-Host "[WARN] Ollama + ComfyUI đang chạy cùng lúc, VRAM=$memPct% — nguy cơ BSOD!"
        Add-Content -Path $logFile -Value "$timestamp | WARN: Ollama + ComfyUI đồng thời, VRAM=${memPct}%"
    }
    
    # Save state
    $state = @{
        timestamp = $timestamp
        memUsed = $memUsed
        memTotal = $memTotal
        memPct = $memPct
        util = $util
        temp = $temp
    }
    $state | ConvertTo-Json | Out-File -FilePath $stateFile -Encoding UTF8
    
} catch {
    Write-Error "[ERROR] GPU monitor exception: $_"
}
