$ohData = "$env:LOCALAPPDATA\OpenHuman"
$ohWiki = "E:\KY-DATA\OpenClaw\projects\openhuman-wiki"
$logDir = "E:\KY-DATA\OpenClaw\logs\oh-sync"
$date = Get-Date -Format 'yyyy-MM-dd_HHmm'
$logFile = "$logDir\sync-$date.log"

Write-Output "[$date] OH Wiki sync starting" | Out-File $logFile

# Check if OpenHuman wiki exists
$ohWikiSrc = "$env:APPDATA\OpenHuman\obsidian-wiki"
if (Test-Path $ohWikiSrc) {
    Write-Output "Found OH wiki at $ohWikiSrc" | Out-File $logFile -Append
    $count = (Get-ChildItem $ohWikiSrc -Recurse -Filter '*.md').Count
    Write-Output "Wiki has $count markdown files" | Out-File $logFile -Append
} else {
    Write-Output "No OH wiki yet - run OpenHuman first to generate it" | Out-File $logFile -Append
}

Write-Output "Sync check complete" | Out-File $logFile -Append
