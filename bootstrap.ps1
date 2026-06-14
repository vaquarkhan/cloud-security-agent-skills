$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
Write-Host "==> cloud-security-agent-skills bootstrap v0.2.0"
python -m pip install -e ".[dev]"
if ($args.Count -gt 0) {
  bash "$Root/scripts/install.sh" @args
} else {
  bash "$Root/scripts/install.sh" all
}
if (Get-Command mcp-bastion -ErrorAction SilentlyContinue) {
  mcp-bastion validate --config bastion.yaml
}
Write-Host "==> Run: cloud-security-agent"
