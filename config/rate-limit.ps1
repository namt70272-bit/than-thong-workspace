# LLM Rate Governor Config
# Auto-set when workspace loads (dot-source this in profile)

# Rate limit
$env:LLM_MAX_CALLS_PER_MINUTE = "30"

# Billing mode: live | dry-run | audit
$env:LLM_BILLING_MODE = "live"

# Daily budget in cents (0 = unlimited)
# $env:LLM_DAILY_BUDGET_CENTS = "500"

# Approved models (comma-separated, empty = all)
# $env:LLM_APPROVED_MODELS = "deepseek,openai"

# Governor config
$env:OPENCLAW_WORKSPACE = Join-Path $PSScriptRoot ".." -Resolve
$env:LLM_GOVERNOR_TIMEOUT = "5"

Write-Host "[Governor] Rate: 30/min | Billing: $env:LLM_BILLING_MODE | Budget: $(if ($env:LLM_DAILY_BUDGET_CENTS) { '$'+[math]::Round([int]$env:LLM_DAILY_BUDGET_CENTS/100,2)+'/day' } else { 'unlimited' })"
