# Changelog

All notable changes to **cloud-security-agent-skills** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-14

### Added

- **VS Code extension** (`vscode-extension/`) — install toolkit, starter packs, presets, MCP Bastion templates
- **JetBrains plugin** (`jetbrains-plugin/`) — Tools menu installers for IntelliJ-family IDEs
- **registry/install-manifest.json** — plugin manifest with sync script
- **scripts/validate-plugin-manifest.py**, **scripts/install.sh** — family-parity packaging
- **.cursor/rules/** — 4 MDC rules (core, zero-trust, Bastion, WAF routing)
- **.github/copilot-instructions.md** — Copilot routing
- **hooks/** — session start + static-secret guard
- **templates/**, **references/**, **mcp/** — Bastion MCP client templates
- **docs/** — cursor, vscode, jetbrains, plugin-publishing, sme-review setup guides
- **Makefile** — validate, demo, plugin-sync targets
- **README** — compliance-family layout with badges, presets, plugin install sections

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
