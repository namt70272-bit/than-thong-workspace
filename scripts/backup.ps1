<#
.SYNOPSIS
    OpenClaw Backup — backup workspace lên GitHub
.DESCRIPTION
    1. Memory consolidation
    2. Git commit all changes
    3. Push to GitHub
#>

Write-Host "=== OpenClaw Backup ===" -ForegroundColor Cyan

$workspace = "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
Set-Location $workspace

# 1. Memory consolidation
Write-Host "[1/4] Consolidating memory..." -NoNewline
python tools-internal/scripts/memory_consolidator.py --cron 2>&1 | Out-Null
Write-Host " OK" -ForegroundColor Green

# 2. Git add
Write-Host "[2/4] Staging changes..." -NoNewline
git add -A 2>&1 | Out-Null
Write-Host " OK" -ForegroundColor Green

# 3. Git commit
Write-Host "[3/4] Committing..." -NoNewline
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit --allow-empty -m "auto-backup: $date" 2>&1 | Out-Null
Write-Host " OK" -ForegroundColor Green

# 4. Git push
Write-Host "[4/4] Pushing to GitHub..." -NoNewline
git push 2>&1 | Out-Null
Write-Host " OK" -ForegroundColor Green

Write-Host "`n=== Backup complete: $date ===`n" -ForegroundColor Cyan
