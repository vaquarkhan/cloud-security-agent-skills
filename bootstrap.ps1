$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Host "==> cloud-security-agent-skills bootstrap"
python -m pip install -e ".[dev]"
if (Get-Command mcp-bastion -ErrorAction SilentlyContinue) { mcp-bastion validate --config bastion.yaml }
$count = (Get-ChildItem -Path skills -Recurse -Filter SKILL.md).Count
Write-Host "==> Skills: $Root\skills\ ($count skills)"
Write-Host "==> Run: cloud-security-agent"
