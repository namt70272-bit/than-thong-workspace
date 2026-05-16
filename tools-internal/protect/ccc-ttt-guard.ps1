#!/usr/bin/env pwsh
param(
    [ValidateSet('status','repair','soft-lock','soft-unlock','hard-lock','hard-unlock','enforce')]
    [string]$Action = 'enforce'
)

$ErrorActionPreference = 'Stop'
$Workspace = 'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
$CanonicalDir = Join-Path $Workspace 'tools-internal\protect\canonical'
$LiveDir = 'E:\KY-DATA\OpenClaw\bin'
$LegacyDir = Join-Path $env:APPDATA 'npm'
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$CurrentSid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$Targets = @(
    @{ Name = 'ccc.ps1'; Canonical = (Join-Path $CanonicalDir 'ccc.ps1'); Live = (Join-Path $LiveDir 'ccc.ps1'); Legacy = (Join-Path $LegacyDir 'ccc.ps1') },
    @{ Name = 'ccc.cmd'; Canonical = (Join-Path $CanonicalDir 'ccc.cmd'); Live = (Join-Path $LiveDir 'ccc.cmd'); Legacy = (Join-Path $LegacyDir 'ccc.cmd') },
    @{ Name = 'ttt.ps1'; Canonical = (Join-Path $CanonicalDir 'ttt.ps1'); Live = (Join-Path $LiveDir 'ttt.ps1'); Legacy = (Join-Path $LegacyDir 'ttt.ps1') },
    @{ Name = 'ttt.cmd'; Canonical = (Join-Path $CanonicalDir 'ttt.cmd'); Live = (Join-Path $LiveDir 'ttt.cmd'); Legacy = (Join-Path $LegacyDir 'ttt.cmd') }
)

function Test-SameHash {
    param([string]$A, [string]$B)
    if (!(Test-Path $A) -or !(Test-Path $B)) { return $false }
    return (Get-FileHash $A -Algorithm SHA256).Hash -eq (Get-FileHash $B -Algorithm SHA256).Hash
}

function Set-ReadOnlyFlag {
    param([string]$Path, [bool]$Enabled)
    if (!(Test-Path $Path)) { return }
    $item = Get-Item $Path -Force
    if ($Enabled) {
        $item.Attributes = $item.Attributes -bor [System.IO.FileAttributes]::ReadOnly
    } else {
        $item.Attributes = $item.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
    }
}

function Invoke-Icacls {
    param([string[]]$Args)
    $out = & icacls @Args 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw ("icacls failed: " + ($out -join "`n"))
    }
}

function Set-HardLock {
    param([string]$Path)
    if (!(Test-Path $Path)) { return }
    Set-ReadOnlyFlag -Path $Path -Enabled:$false
    Invoke-Icacls @($Path, '/inheritance:d')
    Invoke-Icacls @($Path, '/remove:g', 'NT AUTHORITY\Authenticated Users')
    Invoke-Icacls @($Path, '/grant:r', '*'+$CurrentSid+':(RX)')
    Invoke-Icacls @($Path, '/grant:r', 'BUILTIN\Users:(RX)')
    Invoke-Icacls @($Path, '/grant:r', 'BUILTIN\Administrators:(F)')
    Invoke-Icacls @($Path, '/grant:r', 'NT AUTHORITY\SYSTEM:(F)')
    Set-ReadOnlyFlag -Path $Path -Enabled:$true
}

function Clear-HardLock {
    param([string]$Path)
    if (!(Test-Path $Path)) { return }
    Invoke-Icacls @($Path, '/grant:r', '*'+$CurrentSid+':(F)')
    Invoke-Icacls @($Path, '/grant:r', 'BUILTIN\Users:(RX)')
    Invoke-Icacls @($Path, '/grant:r', 'BUILTIN\Administrators:(F)')
    Invoke-Icacls @($Path, '/grant:r', 'NT AUTHORITY\SYSTEM:(F)')
    Set-ReadOnlyFlag -Path $Path -Enabled:$false
}

function Sync-One {
    param($Target)
    if (Test-Path $Target.Live) {
        Clear-HardLock -Path $Target.Live
    }
    if (-not (Test-SameHash $Target.Canonical $Target.Live)) {
        Copy-Item -LiteralPath $Target.Canonical -Destination $Target.Live -Force
    }
}

function Get-OneStatus {
    param($Target)
    $exists = Test-Path $Target.Live
    $same = if ($exists) { Test-SameHash $Target.Canonical $Target.Live } else { $false }
    $readonly = if ($exists) { ((Get-Item $Target.Live -Force).Attributes -band [System.IO.FileAttributes]::ReadOnly) -ne 0 } else { $false }
    $acl = if ($exists) { (icacls $Target.Live | Out-String) } else { '' }
    [pscustomobject]@{
        name = $Target.Name
        exists = $exists
        matchesCanonical = $same
        readOnly = $readonly
        live = $Target.Live
        canonical = $Target.Canonical
        legacy = $Target.Legacy
        acl = $acl.Trim()
    }
}

switch ($Action) {
    'status' {
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'repair' {
        $Targets | ForEach-Object { Sync-One $_ }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'soft-lock' {
        $Targets | ForEach-Object { if (Test-Path $_.Live) { Set-ReadOnlyFlag -Path $_.Live -Enabled:$true } }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'soft-unlock' {
        $Targets | ForEach-Object { if (Test-Path $_.Live) { Set-ReadOnlyFlag -Path $_.Live -Enabled:$false } }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'hard-lock' {
        $Targets | ForEach-Object { if (Test-Path $_.Live) { Set-HardLock -Path $_.Live } }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'hard-unlock' {
        $Targets | ForEach-Object { if (Test-Path $_.Live) { Clear-HardLock -Path $_.Live } }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
    'enforce' {
        $Targets | ForEach-Object { Sync-One $_ }
        $Targets | ForEach-Object { Set-HardLock -Path $_.Live }
        $Targets | ForEach-Object { Get-OneStatus $_ } | ConvertTo-Json -Depth 5
        break
    }
}
