# OpenClaw Operating Guide

## How to Start the System

### 1. Docker Services
Docker Desktop starts automatically with Windows. Verify:
```
docker ps
```
Expected running containers:
- `qdrant` - Vector database (ports 6333-6334)
- `dozzle` - Docker log viewer (port 8888)
- `portainer` - Docker management UI (port 9000)
- `openclaw-tinyproxy` - Proxy (port 1080)

### 2. Local Services

| Service | Start Command | Port | Auto-start |
|---|---|---|---|
| **Ollama** (local LLM) | `ollama serve` | 11434 | Windows service |
| **GitHub Runner** | `runner\run.cmd` | - | Startup shortcut + Windows service |
| **OpenClaw Gateway** | `ccc gateway start` | 18789 | Manual |

### 3. Verify Everything is Running

```powershell
# Check Docker
docker ps

# Check Ollama
curl.exe -s http://localhost:11434/api/tags

# Check Qdrant
curl.exe -s http://localhost:6333

# Check GitHub Runner
Get-Service GitHubActionsRunner

# Check listening ports (our services)
netstat -ano | Select-String "LISTENING" | Select-String "6333|6334|11434|8888|9000|1080|18789"
```

## How to Stop the System

```powershell
# Stop Docker containers (one by one)
docker stop qdrant dozzle portainer openclaw-tinyproxy

# Stop Ollama
taskkill /F /IM ollama.exe

# Stop GitHub Runner
Stop-Service GitHubActionsRunner

# Stop OpenClaw Gateway
ccc gateway stop
```

## How to Check Health

### Quick Health
```powershell
# Docker health
docker ps --format "table {{.Names}}\t{{.Status}}"

# Disk health
Get-PSDrive C,E | Select-Object Name, @{N="FreeGB";E={[math]::Round($_.Free/1GB,1)}}

# Memory
$os = Get-CimInstance Win32_OperatingSystem
[math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory)/1MB, 1)
```

### GitHub Actions Health Check
The `health-check.yml` workflow runs daily at 07:00 and checks:
- Python syntax errors
- Pip dependency conflicts
- Runner service status
- Disk space (>90% warns)
- GitHub token validity

## How to Check Docker

```powershell
# All containers
docker ps -a

# Container logs
docker logs qdrant --tail 50

# Container resource usage
docker stats --no-stream

# Docker system
docker system df
```

### Web UIs

| Service | URL | Auth |
|---|---|---|
| **Portainer** | http://localhost:9000 | Set on first login |
| **Dozzle** | http://localhost:8888 | None (local only) |
| **Ollama** | http://localhost:11434 | None (local API) |

## How to Check Ports

```powershell
# Our service ports
@(6333, 6334, 11434, 8888, 9000, 1080, 18789) | ForEach-Object {
    $p = netstat -ano | Select-String "LISTENING" | Select-String ":$_ "
    if ($p) {
        $pid = ($p -split '\s+')[-1]
        $proc = Get-Process -Id $pid
        "$_ : $($proc.ProcessName)"
    } else {
        "$_ : NOT LISTENING"
    }
}
```

## How to Check Browser Tool

The system uses **Playwright** (Python) for web automation:
```powershell
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); print(f'Playwright OK: chromium {b.version}'); b.close(); p.stop()"
```

## How to Check Local LLM

```powershell
# List models
ollama list

# Test model
curl.exe -s http://localhost:11434/api/generate -d "{\"model\":\"gemma3:1b-it-qat\",\"prompt\":\"say hi\",\"stream\":false}"
```

## Common Errors & Fixes

### Error: "Cannot connect to Docker daemon"
**Fix:** Start Docker Desktop from Start Menu, wait 30s, retry.

### Error: "Port already in use"
**Fix:** Find and stop the conflicting process:
```powershell
netstat -ano | Select-String ":6333 "
taskkill /PID <PID> /F
```

### Error: "Runner not online"
**Fix:** Restart the runner service:
```powershell
Restart-Service GitHubActionsRunner
```

### Error: "Ollama model not found"
**Fix:** Pull the model:
```powershell
ollama pull qwen2.5-coder:7b
```

### Error: "Token expired"
**Fix:** Re-authenticate gh CLI:
```powershell
echo <token> | gh auth login --with-token
```

## How to Backup

### Automatic
`auto-backup.yml` runs daily at 22:00, consolidates memory, commits, and pushes.

### Manual
```powershell
cd "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
git add -A
git commit -m "manual-backup $(Get-Date -Format yyyy-MM-dd)"
git push
```

## How to Re-Audit

```powershell
cd "E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
python tools-internal/scripts/memory_consolidator.py
python tools-internal/scripts/workspace_rag.py --index
```

## Safety Rules for Browser Automation

1. **Never** use the personal browser profile for automation
2. **Always** use headless mode by default
3. **Never** expose Dozzle/Portainer ports to the internet
4. **Never** log API keys or tokens
5. **Always** verify URLs before navigating (no phishing)
6. **Never** auto-fill credentials on unknown sites
7. **Always** set timeouts (max 30s per page load)
8. **Never** download files without user consent

## Quick Reference

```powershell
# Everything running? Quick check:
docker ps -q | wc -l                          # Should be >= 4
curl.exe -s http://localhost:11434 > $null     # Ollama OK
Get-Service GitHubActionsRunner | ? Status -eq "Running"  # Runner OK
```
