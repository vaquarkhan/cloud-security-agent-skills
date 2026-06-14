"""Bastion-protected MCP server for cloud security tool surfaces."""

from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def create_server():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("cloud-security-agent")

    try:
        from agent.bastion_wrapper import bastion_tool

        bastion_available = True
    except ImportError:
        logger.warning("mcp-bastion-python not installed; running without Bastion (dev only)")
        bastion_available = False

        def bastion_tool(name: str):  # type: ignore[misc]
            def decorator(fn):
                return fn

            return decorator

    @mcp.tool()
    @bastion_tool("echo_security_context")
    def echo_security_context(message: str) -> str:
        """Echo security context for integration tests (PII redacted outbound)."""
        return message

    @mcp.tool()
    @bastion_tool("assess_cloud_posture")
    def assess_cloud_posture(cloud: str, scope: str) -> dict:
        """Run a cloud security posture assessment stub for the given provider and scope."""
        skill_map = {
            "aws": "aws-security-best-practices",
            "azure": "azure-security-best-practices",
            "gcp": "gcp-security-best-practices",
            "oci": "oci-oracle-cloud-security",
            "ibm": "ibm-cloud-security-best-practices",
            "alibaba": "alibaba-cloud-security-best-practices",
            "pcf": "vmware-tanzu-pcf-security",
        }
        return {
            "cloud": cloud,
            "scope": scope,
            "status": "review_required",
            "skill": skill_map.get(cloud.lower(), "multi-cloud-security-posture"),
            "checks": ["identity", "network", "encryption", "logging", "iam"],
        }

    @mcp.tool()
    @bastion_tool("validate_security_controls")
    def validate_security_controls(control_area: str, framework: str) -> dict:
        """Validate security controls against a framework (zero-trust, CIS, etc.)."""
        return {
            "control_area": control_area,
            "framework": framework,
            "status": "pending",
            "skill": "mcp-bastion-security-gateway",
        }

    @mcp.resource("config://agent")
    def agent_config() -> str:
        return json.dumps({
            "zero_trust": True,
            "static_secrets": False,
            "repo": "cloud-security-agent-skills",
            "specialization": "multi-cloud-security",
        })

    if bastion_available:
        logger.info("MCP server secured with Bastion tool wrappers")

    return mcp


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")
    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
