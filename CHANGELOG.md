# Changelog

All notable changes to **cloud-security-agent-skills** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-14

### Added

- **14 end-to-end security skills** for AWS, Azure, GCP, OCI, IBM Cloud (Bluemix), Alibaba, VMware Tanzu/PCF, zero-trust identity, Well-Architected frameworks, multi-cloud posture, Bastion gateway, MCP test harness, and AIV PR gate
- **`security/` IdentityManager** — ephemeral credentials for 7 clouds (no static keys)
- **MCP-Bastion gateway** — `bastion.yaml`, `bastion_proxy.py`, tool wrappers
- **MCP server** — `assess_cloud_posture`, `validate_security_controls`, `echo_security_context`
- **Unit tests** (8) and MCP integration tests (protocol + security)
- **CI workflow** — unit tests, Bastion validate, mcp-test harness, AIV gate
- **Per-cloud reference checklists** under `skills/*/references/`
- **Well-Architected pillar matrix** — cross-cloud WAF mapping including Bluemix and PCF legacy names
- **Governance layer** — LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, SUPPORT
- **`scripts/validate-skills.py`** and **`scripts/validate-assets.py`**
- **Presets**, **starter-packs**, **examples/mock-posture-check**
- **Multi-IDE surfaces** — CLAUDE.md, `.claude/commands/`, `.gemini/commands/`, `.kiro/steering/`
- **Dependabot**, **CodeQL**, **pre-commit**, **`requirements-lock.txt`**
- **`registry/provenance.yaml`** — SME source trail for checklists
- **`evals/benchmark/`** — reproducible skill-routing benchmark

[0.1.0]: https://github.com/vaquarkhan/cloud-security-agent-skills/releases/tag/v0.1.0
