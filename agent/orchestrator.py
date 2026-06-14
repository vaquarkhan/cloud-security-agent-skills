"""Cloud Security Agent orchestrator."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Sequence

from agent.bastion_gateway import BastionGateway
from agent.skills_loader import CORE_SECURITY_SKILLS, SkillBundle, SkillsLoader
from security.base import CloudCredentials, IdentityManager
from security.introspection import CloudEnvironment, detect_cloud_environment, get_identity_manager

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Runtime configuration for the Cloud Security Agent."""

    skills_path: Optional[str] = None
    bastion_config: str = "bastion.yaml"
    upstream_mcp_command: Sequence[str] = field(
        default_factory=lambda: ["python", "-m", "agent.mcp_server"]
    )
    force_cloud: Optional[CloudEnvironment] = None


class CloudSecurityAgent:
    """
    Zero-trust multi-cloud security agent orchestrator.

    - Detects cloud environment and routes to IdentityManager
    - Routes all MCP traffic through MCP-Bastion
    - Loads security skills from local skills/ (AWS, Azure, GCP, OCI, IBM, Alibaba, PCF)
    - Integrates mcp-test-harness and AIV gate via tooling skills
    """

    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        self.config = config or AgentConfig()
        self._identity_manager: Optional[IdentityManager] = None
        self._gateway = BastionGateway(
            config_path=Path(self.config.bastion_config),
            upstream_command=list(self.config.upstream_mcp_command),
        )
        skills_root = Path(self.config.skills_path) if self.config.skills_path else None
        self._skills = SkillsLoader(skills_root=skills_root) if skills_root else SkillsLoader()

    @property
    def gateway(self) -> BastionGateway:
        return self._gateway

    @property
    def skills(self) -> SkillsLoader:
        return self._skills

    def introspect_environment(self) -> CloudEnvironment:
        signal = detect_cloud_environment()
        logger.info("Cloud introspection: environment=%s signals=%s", signal.environment.value, signal.signals)
        return signal.environment

    def initialize_identity(self) -> IdentityManager:
        if self._identity_manager is None:
            self._identity_manager = get_identity_manager(self.config.force_cloud)
            logger.info("Identity manager: %s", self._identity_manager.provider_name())
        return self._identity_manager

    def get_cloud_credentials(self) -> CloudCredentials:
        return self.initialize_identity().get_credentials()

    def load_security_skills(self) -> list[SkillBundle]:
        bundles = self._skills.load_core_skills()
        logger.info("Loaded %d security skills", len(bundles))
        return bundles

    def load_cloud_skill(self) -> Optional[SkillBundle]:
        env = self.introspect_environment()
        if env == CloudEnvironment.UNKNOWN:
            return self._skills.load_skill("multi-cloud-security-posture")
        return self._skills.load_for_cloud(env.value)

    def mcp_launch_command(self) -> list[str]:
        return self._gateway.server_entrypoint_argv(self.config.upstream_mcp_command)

    def build_system_context(self) -> str:
        env = self.introspect_environment()
        skills = self.load_security_skills()
        cloud_skill = self.load_cloud_skill()
        sections = [
            "# Cloud Security Agent — Zero Trust Session",
            f"Detected cloud: {env.value}",
            "",
            "## Active Security Skills",
            "",
        ]
        for skill in skills:
            sections.append(f"### {skill.name}")
            sections.append(skill.description or "")
            sections.append("")
        if cloud_skill:
            sections.append(f"## Primary cloud skill: {cloud_skill.name}")
            sections.append("")
        sections.append("## Skill load order")
        sections.append(" → ".join(CORE_SECURITY_SKILLS))
        return "\n".join(sections)

    def validate_security_posture(self) -> dict[str, Any]:
        results: dict[str, Any] = {
            "bastion_valid": self._gateway.validate_config(),
            "cloud_environment": self.introspect_environment().value,
            **self._skills.status(),
            "mcp_command": self.mcp_launch_command(),
        }
        cloud_skill = self.load_cloud_skill()
        if cloud_skill:
            results["primary_cloud_skill"] = cloud_skill.name
        try:
            creds = self.get_cloud_credentials()
            results["identity_provider"] = creds.provider
            results["credentials_ephemeral"] = True
        except Exception as exc:
            results["identity_error"] = str(exc)
        return results


# Backward-compatible alias
DataEngineeringAgent = CloudSecurityAgent


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    agent = CloudSecurityAgent()
    posture = agent.validate_security_posture()
    print("Cloud Security Agent — posture:")
    for key, value in posture.items():
        print(f"  {key}: {value}")
    print("\nMCP clients must use:")
    print(" ", " ".join(agent.mcp_launch_command()))


if __name__ == "__main__":
    main()
