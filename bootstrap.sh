#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "==> cloud-security-agent-skills bootstrap v0.2.0"
PYTHON="${PYTHON:-python3}"
command -v python3 >/dev/null 2>&1 || PYTHON=python
"$PYTHON" -m pip install -e ".[dev]"
if [[ $# -gt 0 ]]; then
  bash "$ROOT/scripts/install.sh" "$@"
else
  bash "$ROOT/scripts/install.sh" all
fi
command -v mcp-bastion >/dev/null 2>&1 && mcp-bastion validate --config bastion.yaml || true
echo "==> Skills: $(find skills -name SKILL.md | wc -l | tr -d ' ') | Run: cloud-security-agent"
