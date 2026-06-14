#!/usr/bin/env python3
"""Validate all SKILL.md files — frontmatter, structure, duplicates, core registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

# Import expected skill list from package when available; fallback for standalone runs
try:
    sys.path.insert(0, str(ROOT))
    from agent.skills_loader import CORE_SECURITY_SKILLS, CLOUD_SECURITY_SKILLS
except ImportError:
    CORE_SECURITY_SKILLS = tuple(
        p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
    ) if SKILLS_DIR.is_dir() else ()
    CLOUD_SECURITY_SKILLS = tuple(
        s for s in CORE_SECURITY_SKILLS
        if s.endswith("-security") or "security-best-practices" in s or s == "oci-oracle-cloud-security"
    )

REQUIRED_FRONTMATTER = ("name", "description")
MIN_BODY_LINES = 35
FORBIDDEN_STRINGS = ("Made-with: Cursor", "Made with Cursor", "Co-authored-by: Cursor")


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def h2_headings(content: str) -> list[str]:
    return re.findall(r"^## .+$", content, re.MULTILINE)


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    skill_name = path.parent.name
    fm = parse_frontmatter(content)

    if not fm:
        errors.append("missing YAML frontmatter (--- block)")
        return errors

    for key in REQUIRED_FRONTMATTER:
        if key not in fm or not fm[key]:
            errors.append(f"missing frontmatter '{key}'")
        elif key == "name" and fm[key] != skill_name:
            errors.append(f"name '{fm[key]}' != directory '{skill_name}'")

    body = content.split("---", 2)[-1] if content.startswith("---") else content
    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    if len(body_lines) < MIN_BODY_LINES:
        errors.append(f"body too short ({len(body_lines)} lines, min {MIN_BODY_LINES})")

    if "## Overview" not in content and "# " not in content.split("---", 2)[-1][:200]:
        errors.append("missing ## Overview or top-level heading")

    headings = h2_headings(content)
    if len(headings) != len(set(headings)):
        dupes = {h for h in headings if headings.count(h) > 1}
        errors.append(f"duplicate H2 headings: {sorted(dupes)}")

    lower = content.lower()
    if skill_name in CLOUD_SECURITY_SKILLS:
        if "checklist" not in lower:
            errors.append("cloud skill missing verification checklist section")
        if "red flag" not in lower:
            errors.append("cloud skill missing red flags section")

    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in content:
            errors.append(f"forbidden attribution string: {forbidden!r}")

    return errors


def validate_registry(skill_dirs: set[str]) -> list[str]:
    errors: list[str] = []
    expected = set(CORE_SECURITY_SKILLS)
    missing_dirs = expected - skill_dirs
    extra_dirs = skill_dirs - expected
    for name in sorted(missing_dirs):
        errors.append(f"core skill missing from skills/: {name}")
    for name in sorted(extra_dirs):
        if (SKILLS_DIR / name / "SKILL.md").is_file():
            errors.append(f"skill directory not in CORE_SECURITY_SKILLS: {name}")
    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: no SKILL.md files found", file=sys.stderr)
        return 1

    skill_dirs = {p.parent.name for p in skill_files}
    total_errors = 0

    for err in validate_registry(skill_dirs):
        total_errors += 1
        print(f"REGISTRY  {err}")

    for skill_path in skill_files:
        errs = validate_skill(skill_path)
        if errs:
            total_errors += len(errs)
            print(f"FAIL {skill_path.relative_to(ROOT)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {skill_path.relative_to(ROOT)}")

    print(f"\nValidated {len(skill_files)} skill(s), {total_errors} error(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
