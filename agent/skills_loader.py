"""Load security skills from the local skills/ directory only."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

import yaml

# Meta + cross-cutting
META_SKILLS = (
    "using-cloud-security-agent-skills",
    "cloud-well-architected-frameworks",
    "zero-trust-identity-and-secrets",
    "multi-cloud-security-posture",
)

# Per-cloud security best practices
CLOUD_SECURITY_SKILLS = (
    "aws-security-best-practices",
    "azure-security-best-practices",
    "gcp-security-best-practices",
    "oci-oracle-cloud-security",
    "ibm-cloud-security-best-practices",
    "alibaba-cloud-security-best-practices",
    "vmware-tanzu-pcf-security",
)

# Tooling layer (Bastion, MCP test harness, AIV gate)
TOOLING_SKILLS = (
    "mcp-bastion-security-gateway",
    "mcp-security-testing-harness",
    "pr-integrity-aiv-gate",
)

CORE_SECURITY_SKILLS = META_SKILLS + CLOUD_SECURITY_SKILLS + TOOLING_SKILLS


@dataclass
class SkillBundle:
    name: str
    description: str
    path: Path
    body: str
    frontmatter: dict = field(default_factory=dict)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@dataclass
class SkillsLoader:
    """Discovers and loads skills from skills/ in this repository only."""

    skills_root: Path = field(default_factory=lambda: repo_root() / "skills")

    def __post_init__(self) -> None:
        env_path = os.getenv("SKILLS_PATH")
        if env_path:
            self.skills_root = Path(env_path)

    def list_available_skills(self) -> list[str]:
        if not self.skills_root.is_dir():
            return list(CORE_SECURITY_SKILLS)
        return sorted(p.name for p in self.skills_root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())

    def list_by_group(self) -> dict[str, list[str]]:
        available = set(self.list_available_skills())
        return {
            "meta": [s for s in META_SKILLS if s in available],
            "cloud": [s for s in CLOUD_SECURITY_SKILLS if s in available],
            "tooling": [s for s in TOOLING_SKILLS if s in available],
        }

    def load_core_skills(self) -> list[SkillBundle]:
        bundles: list[SkillBundle] = []
        for name in CORE_SECURITY_SKILLS:
            bundle = self.load_skill(name)
            if bundle is not None:
                bundles.append(bundle)
        return bundles

    def load_skill(self, name: str) -> Optional[SkillBundle]:
        skill_file = self.skills_root / name / "SKILL.md"
        if not skill_file.is_file():
            return None
        raw = skill_file.read_text(encoding="utf-8")
        frontmatter, body = self._parse_frontmatter(raw)
        return SkillBundle(
            name=name,
            description=str(frontmatter.get("description", "")),
            path=skill_file,
            body=body.strip(),
            frontmatter=frontmatter,
        )

    def load_for_cloud(self, cloud: str) -> Optional[SkillBundle]:
        mapping = {
            "aws": "aws-security-best-practices",
            "azure": "azure-security-best-practices",
            "gcp": "gcp-security-best-practices",
            "oci": "oci-oracle-cloud-security",
            "ibm": "ibm-cloud-security-best-practices",
            "alibaba": "alibaba-cloud-security-best-practices",
            "pcf": "vmware-tanzu-pcf-security",
        }
        skill_name = mapping.get(cloud.lower())
        return self.load_skill(skill_name) if skill_name else None

    def iter_skills(self) -> Iterator[SkillBundle]:
        for name in self.list_available_skills():
            bundle = self.load_skill(name)
            if bundle is not None:
                yield bundle

    def status(self) -> dict[str, object]:
        available = self.list_available_skills()
        missing = [s for s in CORE_SECURITY_SKILLS if s not in available]
        return {
            "skills_root": str(self.skills_root),
            "available_count": len(available),
            "core_expected": len(CORE_SECURITY_SKILLS),
            "missing_skills": missing,
            "skills_complete": len(missing) == 0,
            "groups": self.list_by_group(),
        }

    def _parse_frontmatter(self, raw: str) -> tuple[dict, str]:
        if not raw.startswith("---"):
            return {}, raw
        parts = raw.split("---", 2)
        if len(parts) < 3:
            return {}, raw
        return yaml.safe_load(parts[1]) or {}, parts[2]
