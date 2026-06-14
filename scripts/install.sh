#!/usr/bin/env bash
# Install cloud-security-agent-skills surfaces into the current project.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TARGET="${1:-all}"
DEST="${2:-.}"

copy_files() {
  local label="$1"
  shift
  for rel in "$@"; do
    local src="$ROOT/$rel"
    local dst="$DEST/$rel"
    if [[ -f "$src" ]]; then
      mkdir -p "$(dirname "$dst")"
      cp "$src" "$dst"
      echo "  + $rel"
    fi
  done
  echo "==> Installed $label"
}

install_cursor() {
  echo "==> Cursor adapters"
  copy_files "Cursor rules" \
    .cursor/rules/00-cloud-security-core.mdc \
    .cursor/rules/10-zero-trust-identity.mdc \
    .cursor/rules/20-bastion-gateway-required.mdc \
    .cursor/rules/30-cloud-waf-routing.mdc \
    .cursorrules AGENTS.md skills-index.md
}

install_claude() {
  echo "==> Claude adapters"
  copy_files "Claude commands" \
    .claude/commands/posture-check.md \
    .claude/commands/aws-security-review.md \
    CLAUDE.md AGENTS.md
}

install_vscode() {
  echo "==> VS Code / Copilot adapters"
  copy_files "Copilot instructions" \
    .github/copilot-instructions.md AGENTS.md skills-index.md
}

install_mcp() {
  echo "==> MCP templates"
  copy_files "MCP Bastion" \
    mcp/cloud-security-agent.mcp.json \
    mcp/README.md \
    templates/bastion-mcp-client.json \
    bastion.yaml
}

install_hooks() {
  echo "==> Hooks"
  copy_files "hooks" \
    hooks/hooks.json hooks/README.md \
    hooks/session-start.sh hooks/session-start.ps1 \
    hooks/no-static-secrets-guard.sh hooks/no-static-secrets-guard.ps1
}

install_core() {
  echo "==> Core pack (skills + validators)"
  python scripts/sync-install-manifest.py
  export ROOT="$ROOT"
  export DEST="$DEST"
  python - <<'PY'
import json, shutil, os
from pathlib import Path
root = Path(os.environ["ROOT"])
dest = Path(os.environ.get("DEST", ".")).resolve()
manifest = json.loads((root / "registry/install-manifest.json").read_text())
for key in ("core_files", "skill_files"):
    for rel in manifest.get(key, []):
        src = root / rel
        if src.is_file():
            tgt = dest / rel
            tgt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, tgt)
            print(f"  + {rel}")
PY
}

case "$TARGET" in
  cursor) install_cursor ;;
  claude) install_claude ;;
  vscode|copilot) install_vscode ;;
  mcp) install_mcp ;;
  hooks) install_hooks ;;
  core) install_core ;;
  all)
    install_core
    install_cursor
    install_claude
    install_vscode
    install_mcp
    install_hooks
    ;;
  *)
    echo "Usage: $0 [all|cursor|claude|vscode|mcp|hooks|core] [dest-dir]" >&2
    exit 1
    ;;
esac

echo "==> Done. Run: cloud-security-agent"
