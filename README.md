# cloud-security-agent-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](pyproject.toml)
[![Skills](https://img.shields.io/badge/skills-14-orange.svg)](skills-index.md)
[![Zero Trust](https://img.shields.io/badge/zero--trust-identity-green.svg)](#identity)

**Specialized multi-cloud security agent** — 14 local Agent Skills (AWS, Azure, GCP, OCI, IBM Bluemix, Alibaba, PCF/Tanzu Well-Architected), zero-trust identity, MCP-Bastion gateway, mcp-test-harness, and AIV PR gate. **No external skill repos.**

---

## Why this exists

Security agents must not:

- Use static API keys or long-lived secrets
- Connect to MCP tools without a security gateway
- Merge unrelated data-engineering workflows into a security repo
- Skip automated adversarial testing and PR integrity gates

This repository provides:

1. **14 end-to-end security skills** in `skills/` — **`cloud-well-architected-frameworks`** maps all six WAF pillars across AWS, Azure, GCP, OCI, IBM Cloud (Bluemix), Alibaba, and VMware Tanzu (PCF); each cloud skill covers governance, **IAM**, **KMS/vault**, network, compute/K8s, data, logging, detection, compliance, agent/MCP, checklists, and red flags
2. **IdentityManager** — ephemeral credentials for 7 clouds
3. **MCP-Bastion** — PromptGuard, Presidio, rate limits (`bastion.yaml`)
4. **mcp-test-harness** — protocol + security integration tests
5. **AIV gate** — PR logic density and design rules (`.aiv/`)

---

## Quick start

```bash
git clone git@github.com:vaquarkhan/cloud-security-agent-skills.git
cd cloud-security-agent-skills
./bootstrap.sh          # or: .\bootstrap.ps1
cloud-security-agent
```

---

## Project structure

```
cloud-security-agent-skills/
├── skills/                      # 14 security skills (SKILL.md each)
│   ├── using-cloud-security-agent-skills/
│   ├── cloud-well-architected-frameworks/   # one-stop WAF all clouds
│   ├── zero-trust-identity-and-secrets/
│   ├── aws-security-best-practices/
│   ├── azure-security-best-practices/
│   ├── gcp-security-best-practices/
│   ├── oci-oracle-cloud-security/
│   ├── ibm-cloud-security-best-practices/
│   ├── alibaba-cloud-security-best-practices/
│   ├── vmware-tanzu-pcf-security/
│   ├── multi-cloud-security-posture/
│   ├── mcp-bastion-security-gateway/
│   ├── mcp-security-testing-harness/
│   └── pr-integrity-aiv-gate/
├── security/                    # IdentityManager (7 clouds)
├── agent/                       # CloudSecurityAgent, Bastion, MCP server
├── bastion.yaml                 # MCP-Bastion policy
├── tests/                       # unit + mcp-test-harness integration
├── .aiv/                        # AIV PR gate config
├── registry/assets.json         # Skill index
├── skills-index.md
└── AGENTS.md                    # Agent routing (read first)
```

Full map: [docs/folder-structure.md](docs/folder-structure.md)

---

## Skills catalog

See [skills-index.md](skills-index.md).

| Group | Skills |
|-------|--------|
| **Meta** | using-cloud-security-agent-skills, cloud-well-architected-frameworks, zero-trust-identity-and-secrets, multi-cloud-security-posture |
| **Cloud** | aws, azure, gcp, oci, ibm (Bluemix), alibaba, vmware-tanzu-pcf (Pivotal CF) security skills |
| **Tooling** | mcp-bastion-security-gateway, mcp-security-testing-harness, pr-integrity-aiv-gate |

---

## MCP client (Bastion required)

```json
{
  "mcpServers": {
    "cloud-security-agent": {
      "command": "python",
      "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]
    }
  }
}
```

---

## Testing

```bash
pytest tests/unit/ -v
mcp-bastion validate --config bastion.yaml
mcp-test --server-command "python -m agent.mcp_server"
mcp-test-harness stdio --suite security -- python -m agent.mcp_server
```

---

## Documentation

| Doc | Topic |
|-----|-------|
| [AGENTS.md](AGENTS.md) | Agent entry + routing |
| [skills-index.md](skills-index.md) | Full skill catalog |
| [docs/folder-structure.md](docs/folder-structure.md) | Directory map |
| [docs/architecture.md](docs/architecture.md) | Threat model |
| [docs/getting-started.md](docs/getting-started.md) | Bootstrap |

---

## License

MIT
