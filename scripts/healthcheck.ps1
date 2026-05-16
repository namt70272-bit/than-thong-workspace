<#
.SYNOPSIS
    OpenClaw Health Check — kiểm tra toàn bộ hệ thống
.DESCRIPTION
    Kiểm tra Docker containers, Ollama, Qdrant, GitHub Runner,
    disk space, syntax, pip dependencies
#>

$status = @{Total=0; Pass=0; Fail=0}
$report = @()

function Check {
    param($Name, $ScriptBlock)
    $status.Total++
    try {
        $result = & $ScriptBlock
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            $status.Pass++
            Write-Host "  [OK] $Name" -ForegroundColor Green
            $report += "${Name}: PASS"
        } else {
            $status.Fail++
            Write-Host "  [FAIL] ${Name}: ${result}" -ForegroundColor Red
            $report += "${Name}: FAIL - ${result}"
        }
    } catch {
        $status.Fail++
        Write-Host "  [FAIL] ${Name}: $_" -ForegroundColor Red
        $report += "${Name}: FAIL - $_"
    }
}

Write-Host "`n=== OpenClaw Health Check ===`n" -ForegroundColor Cyan

# 1. Docker
Check "Docker Desktop" { docker ps --format "table {{.Names}}\t{{.Status}}" }
Check "Qdrant" { curl.exe -s http://localhost:6333 | Out-Null; $LASTEXITCODE }
Check "Dozzle" { curl.exe -s http://localhost:8888 | Out-Null; $LASTEXITCODE }
Check "Portainer" { curl.exe -s http://localhost:9000 | Out-Null; $LASTEXITCODE }

# 2. Ollama
Check "Ollama API" { curl.exe -s http://localhost:11434/api/tags | Out-Null; $LASTEXITCODE }
Check "Ollama models" { $m = curl.exe -s http://localhost:11434/api/tags | ConvertFrom-Json; $m.models.Count -gt 0 }

# 3. GitHub Runner
Check "Runner service" { (Get-Service GitHubActionsRunner -ErrorAction SilentlyContinue).Status -eq "Running" }

# 4. Python
Check "Python syntax" { Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object { python -c "import ast; ast.parse(open('$($_.FullName)','r',encoding='utf-8').read())" 2>&1 | Out-Null }; $LASTEXITCODE }
Check "Pytest" { python -m pytest tests/ -q | Out-Null; $LASTEXITCODE }

# 5. Disk
$eDrive = Get-PSDrive E
$freeGB = [math]::Round($eDrive.Free/1GB,1)
Check "Disk space (E: $freeGB GB free)" { $freeGB -gt 50 }

Write-Host "`n=== Results: $($status.Pass)/$($status.Total) passed, $($status.Fail) failed ===`n" -ForegroundColor Cyan

if ($status.Fail -gt 0) {
    Write-Host "FAILED CHECKS:" -ForegroundColor Yellow
    $report | Where-Object { $_ -match "FAIL" } | ForEach-Object { Write-Host "  $_" }
}
