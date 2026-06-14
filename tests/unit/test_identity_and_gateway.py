"""Unit tests for identity introspection and Bastion gateway."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agent.bastion_gateway import BastionGateway
from agent.orchestrator import AgentConfig, CloudSecurityAgent
from agent.skills_loader import CORE_SECURITY_SKILLS, SkillsLoader
from security.introspection import CloudEnvironment, detect_cloud_environment


class TestCloudIntrospection:
    def test_detect_oci_from_env(self, monkeypatch):
        monkeypatch.setenv("OCI_RESOURCE_PRINCIPAL_VERSION", "2.2")
        assert detect_cloud_environment().environment == CloudEnvironment.OCI

    def test_detect_ibm_from_env(self, monkeypatch):
        monkeypatch.delenv("OCI_RESOURCE_PRINCIPAL_VERSION", raising=False)
        monkeypatch.setenv("TRUSTED_PROFILE_NAME", "my-profile")
        assert detect_cloud_environment().environment == CloudEnvironment.IBM


class TestSkillsLoader:
    def test_all_core_skills_present(self):
        loader = SkillsLoader()
        status = loader.status()
        assert status["skills_complete"] is True
        assert status["available_count"] == len(CORE_SECURITY_SKILLS)

    def test_load_aws_skill(self):
        bundle = SkillsLoader().load_skill("aws-security-best-practices")
        assert bundle is not None
        assert "IAM" in bundle.body or "identity" in bundle.body.lower()

    def test_load_for_cloud_aws(self):
        bundle = SkillsLoader().load_for_cloud("aws")
        assert bundle is not None
        assert bundle.name == "aws-security-best-practices"


class TestCloudSecurityAgent:
    def test_mcp_launch_uses_bastion_proxy(self):
        cmd = CloudSecurityAgent(AgentConfig()).mcp_launch_command()
        assert "agent.bastion_proxy" in " ".join(cmd)

    def test_system_context_is_security_focused(self):
        ctx = CloudSecurityAgent(AgentConfig()).build_system_context()
        assert "Cloud Security Agent" in ctx
        assert "aws-security-best-practices" in ctx


class TestBastionGateway:
    def test_server_entrypoint_wraps_upstream(self):
        argv = BastionGateway(upstream_command=["python", "-m", "agent.mcp_server"]).server_entrypoint_argv()
        assert "agent.bastion_proxy" in argv
