#!/usr/bin/env python3
"""Validate registry/install-manifest.json — all listed paths must exist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "registry" / "install-manifest.json"


def collect(manifest: dict) -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []
    for p in manifest.get("core_files", []):
        paths.append(("core_files", p))
    for p in manifest.get("skill_files", []):
        paths.append(("skill_files", p))
    for group, items in manifest.get("agent_adapters", {}).items():
        for p in items:
            paths.append((f"agent_adapters.{group}", p))
    for name, items in manifest.get("starter_packs", {}).items():
        for p in items:
            paths.append((f"starter_packs.{name}", p))
    for name, items in manifest.get("mcp_templates", {}).items():
        for p in items:
            paths.append((f"mcp_templates.{name}", p))
    for name, items in manifest.get("runnable_examples", {}).items():
        for p in items:
            paths.append((f"runnable_examples.{name}", p))
    for p in manifest.get("presets", []):
        paths.append(("presets", p))
    return paths


def main() -> int:
    if not MANIFEST.is_file():
        print(f"ERROR: missing {MANIFEST}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = []
    for section, rel in collect(manifest):
        full = ROOT / rel.replace("/", "\\") if sys.platform == "win32" else ROOT / rel
        full = ROOT / rel
        if not full.exists():
            missing.append(f"[{section}] {rel}")
            print(f"MISSING  {rel}")
        else:
            print(f"OK       {rel}")
    print(f"\nChecked {len(collect(manifest))} manifest path(s), {len(missing)} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
