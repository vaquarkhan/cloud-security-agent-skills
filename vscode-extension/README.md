# Cloud Security Agent Skills — VS Code Extension

Install **14 multi-cloud security skills**, presets, Bastion MCP templates, and zero-trust agent adapters into your workspace.

Compatible editors: **VS Code**, **Cursor**, **Windsurf**, **VSCodium**, **GitHub Copilot**.

## Commands

| Command | Installs |
|---------|----------|
| **Install Full Toolkit** | Skills, presets, hooks, MCP templates, adapters, scripts |
| **Install Core Pack** | AGENTS.md, skills, bastion.yaml, validators |
| **Install Agent Adapters** | Cursor rules, Claude commands, Copilot instructions |
| **Install Starter Pack** | AWS / Azure / GCP / Multi-Cloud YAML bundles |
| **Install Cloud Preset** | Single-cloud WAF preset (AWS, Azure, GCP, OCI, IBM Bluemix, Alibaba, PCF) |
| **Install MCP Bastion Templates** | Bastion-wrapped MCP client config |
| **Scaffold Mock Posture Example** | Runnable `examples/mock-posture-check/` |

## Build & install

```bash
cd vscode-extension
npm install
npx @vscode/vsce package
code --install-extension cloud-security-agent-skills-*.vsix
```

Or bootstrap from repo root:

```bash
./bootstrap.sh --target vscode
```

See [docs/vscode-setup.md](../docs/vscode-setup.md).

## Source resolution

- **Local dev:** loads from parent repo checkout
- **Packaged:** downloads from `rawBaseUrl` (GitHub main)

Default: `https://raw.githubusercontent.com/vaquarkhan/cloud-security-agent-skills/main`
