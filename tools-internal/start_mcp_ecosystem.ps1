<#
.SYNOPSIS
    Auto-start MCP Ecosystem — runs at Windows startup
.DESCRIPTION
    Launches all MCP servers + API Gateway
    Uses Python 3.11 (python) - the only version with full package support
#>

$TOOLS = "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
$LOG = "$TOOLS\logs"
$PYTHON = "python"

# Create log directory
New-Item -ItemType Directory -Path $LOG -Force | Out-Null

function Start-McpServer {
    param($Name, $Script, $Port, $LogFile)
    
    $logPath = "$LOG\$LogFile"
    $proc = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*$Script*" }
    
    if ($proc) {
        Write-Host "  [$Name] Already running (PID $($proc.Id))"
        return $proc
    }
    
    $args = @("`"$TOOLS\$Script`"")
    Start-Process -NoNewWindow -FilePath $PYTHON -ArgumentList $args -RedirectStandardOutput $logPath -RedirectStandardError "$logPath.err"
    
    # Wait and check
    Start-Sleep -Seconds 2
    $proc = Get-Process -Name "python" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*$Script*" }
    
    if ($proc) {
        Write-Host "  [$Name] Started on port $Port (PID $($proc.Id))"
    } else {
        Write-Host "  [$Name] FAILED - check $logPath"
    }
    return $proc
}

Write-Host "=== MCP Ecosystem Auto-Start ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# Start all 5 servers in order
Start-McpServer -Name "System"  -Script "agent_mcp_server.py"   -Port 9876 -LogFile "system.log"
Start-McpServer -Name "Memory"  -Script "mcp_memory_server.py"  -Port 9877 -LogFile "memory.log"
Start-McpServer -Name "Search"  -Script "mcp_search_server.py"  -Port 9878 -LogFile "search.log"
Start-McpServer -Name "LLM"     -Script "mcp_llm_server.py"     -Port 9879 -LogFile "llm.log"

# Gateway needs all MCP servers up first
Start-Sleep -Seconds 3
Start-McpServer -Name "Gateway" -Script "api_gateway.py"        -Port 9001 -LogFile "gateway.log"

Write-Host ""
Write-Host "Health check:"
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:9001/health" -TimeoutSec 5 -UseBasicParsing
    $data = $r.Content | ConvertFrom-Json
    Write-Host "  Gateway: $($data.gateway)"
    foreach ($srv in $data.servers.PSObject.Properties) {
        Write-Host "  $($srv.Name): $($srv.Value.status)"
    }
} catch {
    Write-Host "  Gateway not ready yet"
}

Write-Host ""
Write-Host "=== All servers started ==="
