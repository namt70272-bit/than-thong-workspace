#!/usr/bin/env pwsh
# ccc -- OpenClaw from E: drive, fully independent
# Usage: ccc command
# Example: ccc status, ccc hooks list, ccc gateway restart

$Script:OPENCLAW_HOME = "E:\KY-DATA\OpenClaw\runtime-mirror"
$Script:OPENCLAW_WORKSPACE = "$Script:OPENCLAW_HOME\.openclaw\workspace"
$Script:OPENCLAW_CONFIG = "C:\Users\ACER\.openclaw\openclaw.json"
$Script:CODE_MIRROR = "E:\KY-DATA\OpenClaw\code-mirror\npm\node_modules\openclaw"
$Script:OPENCLAW_MJS = "$Script:CODE_MIRROR\openclaw.mjs"
$Script:NODE_EXE = "E:\KY-DATA\OpenClaw\portable-node\node.exe"

$env:OPENCLAW_HOME = $Script:OPENCLAW_HOME
$env:OPENCLAW_WORKSPACE = $Script:OPENCLAW_WORKSPACE
$env:OPENCLAW_CONFIG_PATH = $Script:OPENCLAW_CONFIG

if ($args.Count -eq 0) {
    $args = @('gateway', 'start')
}

# Run OpenClaw from E:
& $Script:NODE_EXE $Script:OPENCLAW_MJS $args
