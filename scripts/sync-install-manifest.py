#!/usr/bin/env python3
"""Sync skill_files in registry/install-manifest.json from skills/ directory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "registry" / "install-manifest.json"
SKILLS = ROOT / "skills"


def discover_skill_files() -> list[str]:
    paths: list[str] = []
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_file():
            paths.append(str(skill_md.relative_to(ROOT)).replace("\\", "/"))
        refs = skill_dir / "references"
        if refs.is_dir():
            for ref in sorted(refs.rglob("*")):
                if ref.is_file():
                    paths.append(str(ref.relative_to(ROOT)).replace("\\", "/"))
    return paths


def main() -> int:
    if not MANIFEST.is_file():
        print(f"ERROR: {MANIFEST} not found", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    discovered = discover_skill_files()
    manifest["skill_files"] = discovered
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    # Copy to extension and jetbrains plugin resources
    for target in (
        ROOT / "vscode-extension" / "install-manifest.json",
        ROOT / "jetbrains-plugin" / "src" / "main" / "resources" / "install-manifest.json",
    ):
        if target.parent.exists():
            target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"Synced {target.relative_to(ROOT)}")
    print(f"Updated skill_files: {len(discovered)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
