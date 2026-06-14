#!/usr/bin/env python3
"""Validate registry/assets.json — ensure all referenced paths exist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "registry" / "assets.json"


def collect_paths(data: dict) -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []

    for group, names in data.get("skill_groups", {}).items():
        for name in names:
            paths.append((f"skill_groups.{group}", f"skills/{name}/SKILL.md"))

    for item in data.get("examples", []):
        paths.append(("examples", item["path"]))
    for item in data.get("presets", []):
        paths.append(("presets", item["path"]))
    for item in data.get("starter_packs", []):
        paths.append(("starter_packs", item["path"]))
    for item in data.get("references", []):
        paths.append(("references", item["path"]))
    for item in data.get("core_scripts", []):
        paths.append(("core_scripts", item))
    for item in data.get("evals", []):
        paths.append(("evals", item["path"]))

    tooling = data.get("tooling", {})
    for key, rel in tooling.items():
        if isinstance(rel, str):
            paths.append((f"tooling.{key}", rel))

    for item in data.get("install_surfaces", []):
        for p in item.get("paths", []):
            paths.append(("install_surfaces", p.rstrip("/")))

    prov = data.get("provenance", {})
    if isinstance(prov.get("registry_file"), str):
        paths.append(("provenance", prov["registry_file"]))

    version_file = data.get("version_file")
    if version_file:
        paths.append(("version_file", version_file))

    return paths


def main() -> int:
    if not ASSETS.exists():
        print(f"ERROR: {ASSETS} not found", file=sys.stderr)
        return 1

    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    paths = collect_paths(data)
    missing: list[str] = []

    for section, rel in paths:
        full = ROOT / rel
        if not full.exists():
            missing.append(f"[{section}] {rel}")
            print(f"MISSING  {rel}")
        else:
            print(f"OK       {rel}")

    print(f"\nChecked {len(paths)} path(s), {len(missing)} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
