$ErrorActionPreference = 'Stop'

$IndexPath = 'E:\skill\_skill-index.csv'
$LogPath = 'E:\skill\_download_log.txt'
$TempRoot = 'E:\skill\_tmp_group_b'
$CategoryMap = @{
  'Specialized Domains' = 'E:\skill\43-Cong-Dong-Chuyen-Nganh-Dac-Thu'
  'Marketing' = 'E:\skill\44-Cong-Dong-Tiep-Thi-Mang-Xa-Hoi'
  'Context Engineering' = 'E:\skill\45-Cong-Dong-Ky-Thuat-Ngu-Canh'
  'n8n Automation' = 'E:\skill\46-Cong-Dong-n8n-Tu-Dong-Hoa'
}

function Safe-Name([string]$s) {
  $x = $s.Trim()
  $x = $x -replace 'https?://',''
  $x = $x -replace '[\\/:*?"<>|]+','__'
  $x = $x -replace '\s+','-'
  $x = $x -replace '[^\p{L}\p{Nd}._-]+','_'
  $x = $x.Trim(' ','.','_','-')
  if ($x.Length -gt 120) { $x = $x.Substring(0,120).Trim(' ','.','_','-') }
  if ([string]::IsNullOrWhiteSpace($x)) { $x = 'unnamed-skill' }
  return $x
}

function Ensure-CleanDir([string]$path) {
  if (Test-Path $path) { Remove-Item $path -Recurse -Force }
  New-Item -ItemType Directory -Force -Path $path | Out-Null
}

function Write-Source([string]$dest,[string]$name,[string]$category,[string]$url,[string]$desc,[string]$status,[string]$reason) {
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  $txt = @"
Skill: $name
Category: $category
Source: $url
Status: $status
Reason: $reason
Description: $desc
DownloadedAt: $((Get-Date).ToString('s'))
"@
  Set-Content -Path (Join-Path $dest 'SOURCE.txt') -Value $txt -Encoding UTF8
}

function Copy-DirectoryContents([string]$src,[string]$dest) {
  Ensure-CleanDir $dest
  Get-ChildItem -LiteralPath $src -Force | Where-Object { $_.Name -ne '.git' } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
  }
}

function Run-Git($argList, [string]$cwd = $null) {
  $old = Get-Location
  $oldPrompt = $env:GIT_TERMINAL_PROMPT
  try {
    $env:GIT_TERMINAL_PROMPT = '0'
    if ($cwd) { Set-Location $cwd }
    $out = & git @argList 2>&1
    $code = $LASTEXITCODE
    return @{ Code=$code; Output=($out -join "`n") }
  } finally {
    $env:GIT_TERMINAL_PROMPT = $oldPrompt
    Set-Location $old
  }
}

function Parse-GitHub([string]$url) {
  try { $u = [System.Uri]$url } catch { return $null }
  if ($u.Host.ToLowerInvariant() -ne 'github.com') { return $null }
  $parts = $u.AbsolutePath.Trim('/') -split '/'
  if ($parts.Count -lt 2) { return $null }
  $owner = $parts[0]; $repo = $parts[1]
  $repoNoGit = $repo -replace '\.git$',''
  $info = [ordered]@{ Owner=$owner; Repo=$repoNoGit; RepoUrl="https://github.com/$owner/$repoNoGit.git"; Kind='repo'; Ref=$null; SubPath=$null; RawUrl=$null }
  if ($parts.Count -ge 5 -and ($parts[2] -eq 'tree' -or $parts[2] -eq 'blob')) {
    $info.Kind = $parts[2]
    $info.Ref = $parts[3]
    $info.SubPath = ($parts[4..($parts.Count-1)] -join '/')
    if ($info.Kind -eq 'blob') { $info.RawUrl = "https://raw.githubusercontent.com/$owner/$repoNoGit/$($info.Ref)/$($info.SubPath)" }
  }
  return $info
}

function Download-GitHubRepo([hashtable]$gh,[string]$dest,[string]$name,[string]$cat,[string]$url,[string]$desc) {
  $tmp = Join-Path $TempRoot ([guid]::NewGuid().ToString())
  try {
    try {
      $api = "https://api.github.com/repos/$($gh.Owner)/$($gh.Repo)"
      Invoke-WebRequest -Uri $api -UseBasicParsing -TimeoutSec 25 | Out-Null
    } catch {
      $status = $null
      try { $status = [int]$_.Exception.Response.StatusCode } catch {}
      if ($status -eq 404) { throw "GitHub repository unavailable/private (API 404): $($gh.Owner)/$($gh.Repo)" }
    }
    if ($gh.Kind -eq 'repo') {
      $r = Run-Git -argList @('clone','--depth','1',$gh.RepoUrl,$tmp)
      if ($r.Code -ne 0) { throw "git clone failed: $($r.Output)" }
      Copy-DirectoryContents $tmp $dest
      Write-Source $dest $name $cat $url $desc 'downloaded' 'shallow cloned repository; .git removed after copy'
      return @{ ok=$true; reason='downloaded' }
    }
    elseif ($gh.Kind -eq 'tree') {
      $r = Run-Git -argList @('clone','--depth','1','--filter=blob:none','--sparse','--branch',$gh.Ref,$gh.RepoUrl,$tmp)
      if ($r.Code -ne 0) { throw "git sparse clone failed: $($r.Output)" }
      $r2 = Run-Git -argList @('sparse-checkout','set','--no-cone',$gh.SubPath) -cwd $tmp
      if ($r2.Code -ne 0) { throw "sparse-checkout failed: $($r2.Output)" }
      $src = Join-Path $tmp ($gh.SubPath -replace '/', [System.IO.Path]::DirectorySeparatorChar)
      if (!(Test-Path $src)) { throw "subfolder not found after sparse checkout: $($gh.SubPath)" }
      Copy-DirectoryContents $src $dest
      Write-Source $dest $name $cat $url $desc 'downloaded' "sparse cloned subfolder $($gh.SubPath) from $($gh.Owner)/$($gh.Repo)@$($gh.Ref); .git removed after copy"
      return @{ ok=$true; reason='downloaded' }
    }
    elseif ($gh.Kind -eq 'blob') {
      Ensure-CleanDir $dest
      $fileName = Split-Path $gh.SubPath -Leaf
      Invoke-WebRequest -Uri $gh.RawUrl -OutFile (Join-Path $dest $fileName) -UseBasicParsing -TimeoutSec 60
      Write-Source $dest $name $cat $url $desc 'downloaded' "downloaded single file $($gh.SubPath) from raw GitHub URL"
      return @{ ok=$true; reason='downloaded' }
    }
  } catch {
    Ensure-CleanDir $dest
    Write-Source $dest $name $cat $url $desc 'unavailable' $_.Exception.Message
    return @{ ok=$false; reason=$_.Exception.Message }
  } finally {
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
  }
}

function Download-NonGit([string]$url,[string]$dest,[string]$name,[string]$cat,[string]$desc) {
  try {
    Ensure-CleanDir $dest
    $leaf = Split-Path ([System.Uri]$url).AbsolutePath -Leaf
    if ([string]::IsNullOrWhiteSpace($leaf)) { $leaf = 'downloaded-skill' }
    Invoke-WebRequest -Uri $url -OutFile (Join-Path $dest $leaf) -UseBasicParsing -TimeoutSec 60
    Write-Source $dest $name $cat $url $desc 'downloaded' 'downloaded non-GitHub URL as single file'
    return @{ ok=$true; reason='downloaded' }
  } catch {
    Ensure-CleanDir $dest
    Write-Source $dest $name $cat $url $desc 'unavailable' $_.Exception.Message
    return @{ ok=$false; reason=$_.Exception.Message }
  }
}

New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
foreach ($d in $CategoryMap.Values) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

$rows = Import-Csv $IndexPath | Where-Object { $CategoryMap.ContainsKey($_.Category) }
$results = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
  $cat = $row.Category; $base = $CategoryMap[$cat]
  $safe = Safe-Name $row.SkillName
  $dest = Join-Path $base $safe
  Write-Host "[$cat] $($row.SkillName)"
  $gh = Parse-GitHub $row.Url
  if ($gh) { $res = Download-GitHubRepo $gh $dest $row.SkillName $cat $row.Url $row.Description }
  else { $res = Download-NonGit $row.Url $dest $row.SkillName $cat $row.Description }
  $results.Add([pscustomobject]@{ Category=$cat; SkillName=$row.SkillName; Url=$row.Url; Dest=$dest; Ok=[bool]$res.ok; Reason=[string]$res.reason }) | Out-Null
}

$stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz')
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('') | Out-Null
$lines.Add("=== GROUP B download run: $stamp ===") | Out-Null
foreach ($cat in $CategoryMap.Keys) {
  $catResults = @($results | Where-Object Category -eq $cat)
  $ok = @($catResults | Where-Object Ok).Count
  $bad = $catResults.Count - $ok
  $folder = $CategoryMap[$cat]
  $lines.Add("$cat -> $folder : downloaded=$ok unavailable=$bad total=$($catResults.Count)") | Out-Null
}
$unavail = @($results | Where-Object { -not $_.Ok })
$lines.Add('Unavailable items:') | Out-Null
if ($unavail.Count -eq 0) { $lines.Add('  none') | Out-Null } else { foreach($u in $unavail){ $lines.Add("  - [$($u.Category)] $($u.SkillName) :: $($u.Url) :: $($u.Reason)") | Out-Null } }
Add-Content -Path $LogPath -Value ($lines -join "`r`n") -Encoding UTF8

$summaryPath = 'E:\skill\_group_b_summary.json'
$results | ConvertTo-Json -Depth 5 | Set-Content -Path $summaryPath -Encoding UTF8
Write-Host "SUMMARY_WRITTEN $summaryPath"
$lines -join "`n" | Write-Host
