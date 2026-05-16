param(
    [string]$message
)
$logPath = "E:\KY-DATA\OpenClaw\logs\watchdog.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$line = "[$timestamp] $message"
Add-Content -Path $logPath -Value $line
Write-Output $line
