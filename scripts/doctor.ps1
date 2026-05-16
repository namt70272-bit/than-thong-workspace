<#
.SYNOPSIS
    OpenClaw Doctor — chẩn đoán lỗi phổ biến
.DESCRIPTION
    Kiểm tra và gợi ý fix cho các lỗi thường gặp
#>

Write-Host "=== OpenClaw Doctor ===`n" -ForegroundColor Cyan
$issues = @()

# 1. Docker
$dockerOk = $false
try { docker ps --format "{{.Names}}" | Out-Null; $dockerOk = $true } catch {}
if (-not $dockerOk) {
    $issues += "Docker Desktop not running. Start Docker Desktop from Start Menu."
}

# 2. Port conflicts
$ports = @{6333="Qdrant"; 11434="Ollama"; 8888="Dozzle"; 9000="Portainer"; 1080="Tinyproxy"}
foreach ($p in $ports.Keys) {
    $used = netstat -ano | Select-String "LISTENING" | Select-String ":$p "
    if (-not $used) {
        $issues += "Port $p ($($ports[$p])) not listening. Service may be down."
    }
}

# 3. Ollama models
try {
    $models = curl.exe -s http://localhost:11434/api/tags | ConvertFrom-Json
    if ($models.models.Count -eq 0) {
        $issues += "Ollama running but no models loaded. Run: ollama pull qwen2.5-coder:7b"
    }
} catch {
    $issues += "Ollama not reachable at localhost:11434. Run: ollama serve"
}

# 4. Git status
$gitStatus = git status --porcelain 2>&1
if ($gitStatus) {
    $count = ($gitStatus | Measure-Object).Count
    $issues += "Git workspace has $count uncommitted changes. Run: git add -A && git commit"
}

# 5. GitHub Runner
try {
    $svc = Get-Service GitHubActionsRunner -ErrorAction SilentlyContinue
    if ($svc.Status -ne "Running") {
        $issues += "GitHub Runner service not running. Run: Start-Service GitHubActionsRunner"
    }
} catch {
    $issues += "GitHub Runner service not installed."
}

# 6. Syntax check
try {
    $errors = 0
    Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object {
        try { python -c "import ast; ast.parse(open('$($_.FullName)','r',encoding='utf-8').read())" 2>&1 | Out-Null }
        catch { $errors++ }
    }
    if ($errors -gt 0) {
        $issues += "$errors Python file(s) with syntax errors."
    }
} catch {}

# Report
if ($issues.Count -eq 0) {
    Write-Host "No issues found. System looks healthy!`n" -ForegroundColor Green
} else {
    Write-Host "Found $($issues.Count) issue(s):`n" -ForegroundColor Yellow
    for ($i = 0; $i -lt $issues.Count; $i++) {
        Write-Host "$($i+1). $($issues[$i])" -ForegroundColor Yellow
    }
}
