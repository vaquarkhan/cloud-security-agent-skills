# cloud-security-agent-skills

<p align="center">
  <strong>Multi-cloud zero-trust security agent</strong><br/>
  14 Agent Skills · IdentityManager · MCP-Bastion · Well-Architected · VS Code & JetBrains plugins
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT"></a>
  <a href="https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml"><img src="https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/codeql-analysis.yml"><img src="https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/codeql-analysis.yml/badge.svg" alt="CodeQL"></a>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/skills-14-orange.svg" alt="Skills">
  <img src="https://img.shields.io/badge/clouds-7-blue.svg" alt="Clouds">
  <a href="VERSION"><img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Well--Architected-232F3E?style=flat&logo=amazonaws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Azure-WAF-0078D4?style=flat&logo=microsoftazure&logoColor=white" alt="Azure">
  <img src="https://img.shields.io/badge/GCP-Architecture-4285F4?style=flat&logo=googlecloud&logoColor=white" alt="GCP">
  <img src="https://img.shields.io/badge/OCI-Security-F80000?style=flat&logo=oracle&logoColor=white" alt="OCI">
  <img src="https://img.shields.io/badge/IBM-Bluemix-052FAD?style=flat&logo=ibm&logoColor=white" alt="IBM">
  <img src="https://img.shields.io/badge/Alibaba-WAF-FF6A00?style=flat&logo=alibabacloud&logoColor=white" alt="Alibaba">
  <img src="https://img.shields.io/badge/Tanzu-PCF-0091DA?style=flat&logo=vmware&logoColor=white" alt="PCF">
</p>

**Zero-trust multi-cloud security for AI agents** — 14 end-to-end Agent Skills, a real **MCP-Bastion** stdio proxy, **IdentityManager** with ephemeral credentials for 7 clouds, Well-Architected framework mappings (AWS · Azure · GCP · OCI · IBM Bluemix · Alibaba · PCF/Tanzu), plus **VS Code** and **JetBrains** install plugins.

> **Disclaimer:** Operational security patterns and automation templates — not a substitute for your cloud QSA, CISO sign-off, or penetration test report.

**Coverage:** IAM, KMS/vault, network, compute/K8s, logging, detection, compliance, and agent/MCP deployment for every major cloud. Provenance trail in [registry/provenance.yaml](registry/provenance.yaml). Full status: [docs/project-status.md](docs/project-status.md).

---

## Why this exists

Security agents must not:

- Embed **static API keys** or long-lived tokens in code or MCP configs
- Connect to MCP tools **without** a security gateway (PII redaction, injection defense)
- Review AWS IAM while ignoring Azure Entra ID or GCP Workload Identity in hybrid estates
- Ship skills without validation, provenance, or IDE install surfaces

**cloud-security-agent-skills** delivers:

1. **14 specialized skills** (~215 lines avg) — deepest end-to-end cloud security content in the agent-skills family
2. **IdentityManager** — thread-safe ephemeral credentials (AWS IRSA, Azure MI, GCP WIF, OCI resource principal, IBM Trusted Profile, Alibaba RAM, PCF CredHub)
3. **MCP-Bastion gateway** — real `bastion_proxy.py` stdio proxy; `bastion.yaml` policy-as-code (Presidio, PromptGuard, RBAC, rate limits)
4. **Well-Architected one-stop shop** — six pillars mapped across all clouds including Bluemix and Pivotal PCF legacy names
5. **IDE plugins** — VS Code extension + JetBrains plugin (install skills, presets, MCP templates, adapters)
6. **Governance** — validators, benchmark, AIV PR gate, CodeQL, Dependabot, pre-commit

---

## Quick start

### Prerequisites

- Python **3.10+**
- Node.js **18+** (VS Code extension build; optional)
- JDK **17+** (JetBrains plugin build; optional)

### Bootstrap (recommended)

**macOS / Linux:**

```bash
git clone git@github.com:vaquarkhan/cloud-security-agent-skills.git
cd cloud-security-agent-skills
chmod +x bootstrap.sh scripts/install.sh
./bootstrap.sh
```

**Windows (PowerShell):**

```powershell
git clone git@github.com:vaquarkhan/cloud-security-agent-skills.git
cd cloud-security-agent-skills
.\bootstrap.ps1
```

Detects your workflow and installs skills, Cursor rules, Claude commands, Copilot instructions, MCP templates, and hooks.

### Run the agent

```bash
pip install -e ".[dev]"
cloud-security-agent
python examples/mock-posture-check/run_posture_check.py
```

### Validate the repository

```bash
make validate
make test
make demo
```

---

## Plugin installation

### Cursor

```bash
./bootstrap.sh --target cursor
```

See [docs/cursor-setup.md](docs/cursor-setup.md) — installs `.cursor/rules/` + skills.

### VS Code / GitHub Copilot

```bash
cd vscode-extension && npm install && npx @vscode/vsce package
code --install-extension cloud-security-agent-skills-*.vsix
```

Or: `./bootstrap.sh --target vscode`

See [docs/vscode-setup.md](docs/vscode-setup.md) · [vscode-extension/README.md](vscode-extension/README.md)

### Claude Code

```bash
./bootstrap.sh --target claude
```

Copies `.claude/commands/` and `CLAUDE.md`.

### JetBrains (IntelliJ, PyCharm, …)

```bash
cd jetbrains-plugin && ./gradlew buildPlugin
```

**Tools → Cloud Security Agent Skills → Install Full Toolkit**

See [docs/jetbrains-setup.md](docs/jetbrains-setup.md) · [jetbrains-plugin/README.md](jetbrains-plugin/README.md)

---

## Security lifecycle commands

| Command | Purpose | Skill / doc |
|---------|---------|-------------|
| `/posture-check` | Skills complete, Bastion valid, routing | `.claude/commands/posture-check.md` |
| `/aws-security-review` | Full AWS IAM/KMS/network review | `.claude/commands/aws-security-review.md` |
| **Assess** | Posture + WAF pillar scoring | `cloud-well-architected-frameworks` |
| **Harden** | Remediate IAM/KMS/network gaps | Per-cloud skill |
| **Validate** | mcp-test security suite | `mcp-security-testing-harness` |
| **Gate** | AIV PR integrity | `pr-integrity-aiv-gate` |

Example flow:

```
/posture-check  →  load cloud skill  →  WAF review  →  mcp-test  →  AIV gate
```

---

## Skills catalog

**14 skills** — full index: [skills-index.md](skills-index.md)

| Group | Skills |
|-------|--------|
| **Meta** | using-cloud-security-agent-skills, **cloud-well-architected-frameworks**, zero-trust-identity-and-secrets, multi-cloud-security-posture |
| **Cloud** | aws, azure, gcp, oci, ibm (Bluemix), alibaba, vmware-tanzu-pcf (Pivotal CF) |
| **Tooling** | mcp-bastion-security-gateway, mcp-security-testing-harness, pr-integrity-aiv-gate |

Each cloud skill: governance → **IAM** → **KMS** → network → compute → data → logging → compliance → checklist → red flags.

---

## Cloud presets & starter packs

| Cloud | Preset | Starter pack |
|-------|--------|--------------|
| AWS | [presets/aws-security/](presets/aws-security/PRESET.md) | [aws-agent-starter.yaml](starter-packs/aws-agent-starter.yaml) |
| Azure | [presets/azure-security/](presets/azure-security/PRESET.md) | [azure-agent-starter.yaml](starter-packs/azure-agent-starter.yaml) |
| GCP | [presets/gcp-security/](presets/gcp-security/PRESET.md) | [gcp-agent-starter.yaml](starter-packs/gcp-agent-starter.yaml) |
| OCI | [presets/oci-security/](presets/oci-security/PRESET.md) | — |
| IBM / Bluemix | [presets/ibm-bluemix-security/](presets/ibm-bluemix-security/PRESET.md) | — |
| Alibaba | [presets/alibaba-security/](presets/alibaba-security/PRESET.md) | — |
| PCF / Tanzu | [presets/tanzu-pcf-security/](presets/tanzu-pcf-security/PRESET.md) | — |
| Multi-cloud | [presets/multi-cloud-hybrid/](presets/multi-cloud-hybrid/PRESET.md) | [multi-cloud-agent-starter.yaml](starter-packs/multi-cloud-agent-starter.yaml) |

---

## Well-Architected frameworks

One-stop cross-cloud WAF: [skills/cloud-well-architected-frameworks/SKILL.md](skills/cloud-well-architected-frameworks/SKILL.md)

Full pillar matrix: [well-architected-pillar-matrix.md](skills/cloud-well-architected-frameworks/references/well-architected-pillar-matrix.md)

| Provider | Framework |
|----------|-----------|
| AWS | AWS Well-Architected Framework |
| Azure | Microsoft Azure Well-Architected Framework |
| GCP | Google Cloud Architecture Framework |
| OCI | OCI Architecture Center |
| IBM | IBM Cloud / Bluemix + SCC |
| Alibaba | Alibaba Cloud Well-Architected |
| PCF | Tanzu Reference Architecture + NIST CSF |

---

## Project structure

```
cloud-security-agent-skills/
├── skills/                    # 14 Agent Skills (SKILL.md each)
├── security/                  # IdentityManager — 7 clouds
├── agent/                     # CloudSecurityAgent, Bastion proxy, MCP server
├── presets/                   # 8 cloud WAF/security presets
├── starter-packs/             # YAML starter bundles
├── examples/mock-posture-check/
├── vscode-extension/          # VS Code / Cursor / Copilot plugin
├── jetbrains-plugin/          # IntelliJ-family plugin
├── registry/
│   ├── assets.json            # Machine-readable index
│   ├── install-manifest.json  # Plugin install manifest
│   └── provenance.yaml        # SME source trail
├── scripts/                   # validate-skills, validate-assets, install
├── evals/benchmark/           # Skill routing benchmark (100% target)
├── hooks/                     # Session + static-secret guards
├── templates/                 # Bastion MCP client, posture checklist
├── references/                # Multi-cloud control matrix
├── mcp/                       # Bastion MCP client template
├── docs/                      # Setup guides per IDE
├── .cursor/rules/             # Cursor agent rules
├── .claude/commands/          # Claude slash commands
├── bastion.yaml               # MCP-Bastion policy
└── AGENTS.md                  # Agent routing (read first)
```

Full map: [docs/folder-structure.md](docs/folder-structure.md)

---

## MCP integrations

Bastion-wrapped MCP — **never** connect directly to `agent.mcp_server`:

| Template | Use case |
|----------|----------|
| [mcp/cloud-security-agent.mcp.json](mcp/cloud-security-agent.mcp.json) | Cursor / Claude Desktop stdio |
| [templates/bastion-mcp-client.json](templates/bastion-mcp-client.json) | Copy-paste client config |

Tools: `assess_cloud_posture`, `validate_security_controls`, `echo_security_context`

See [mcp/README.md](mcp/README.md) and skill `mcp-bastion-security-gateway`.

---

## Examples

| Example | Description |
|---------|-------------|
| [examples/mock-posture-check/](examples/mock-posture-check/) | Multi-cloud posture check — no cloud credentials required |

```bash
python examples/mock-posture-check/run_posture_check.py --cloud aws --cloud azure --json
```

---

## Documentation

| Doc | Topic |
|-----|-------|
| [docs/project-status.md](docs/project-status.md) | Feature list and version summary |
| [docs/architecture.md](docs/architecture.md) | Threat model + data flow |
| [docs/getting-started.md](docs/getting-started.md) | First-run walkthrough |
| [docs/testing.md](docs/testing.md) | Unit + MCP harness + local dev |
| [docs/cursor-setup.md](docs/cursor-setup.md) | Cursor install |
| [docs/vscode-setup.md](docs/vscode-setup.md) | VS Code / Copilot install |
| [docs/jetbrains-setup.md](docs/jetbrains-setup.md) | JetBrains plugin |
| [docs/plugin-publishing.md](docs/plugin-publishing.md) | Release VSIX / plugin ZIP |
| [docs/sme-review.md](docs/sme-review.md) | Provenance cadence |
| [AGENTS.md](AGENTS.md) | Agent entry + routing |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow |
| [SECURITY.md](SECURITY.md) | Vulnerability disclosure |

---

## Identity (zero-trust)

| Cloud | Mechanism | Never use |
|-------|-----------|-----------|
| AWS | IRSA / instance profile | Access keys |
| Azure | Managed identity | Client secret on compute |
| GCP | Workload Identity | Downloaded SA JSON |
| OCI | Resource principal | API signing key in code |
| IBM / Bluemix | Trusted Profile | Service ID API key |
| Alibaba | ECS RAM role / RRSA | AccessKey in env |
| PCF / Tanzu | UAA + CredHub | Secrets in manifest.yml |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgments

Built on [MCP-Bastion](https://github.com/vaquarkhan/MCP-Bastion), [mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness), [aiv-integrity-gate](https://github.com/vaquarkhan/aiv-integrity-gate), and the Agent Skills progressive-disclosure pattern. Packaged like [compliance-agent-skills](https://github.com/vaquarkhan/compliance-agent-skills) for family consistency.
