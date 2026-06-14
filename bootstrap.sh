#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
echo "==> cloud-security-agent-skills bootstrap"
PYTHON="${PYTHON:-python3}"
command -v python3 >/dev/null 2>&1 || PYTHON=python
"$PYTHON" -m pip install -e ".[dev]"
command -v mcp-bastion >/dev/null 2>&1 && mcp-bastion validate --config bastion.yaml || true
echo "==> Skills: $ROOT/skills/ ($(find skills -name SKILL.md | wc -l | tr -d ' ') skills)"
echo "==> Run: cloud-security-agent"
