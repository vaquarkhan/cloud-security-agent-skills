# cloud-security-agent-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/vaquarkhan/cloud-security-agent-skills/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](pyproject.toml)
[![Skills](https://img.shields.io/badge/skills-14-orange.svg)](skills-index.md)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](VERSION)

[![Zero Trust](https://img.shields.io/badge/zero--trust-identity-green.svg)](#identity)

**Version 0.1.0** — see [CHANGELOG.md](CHANGELOG.md) | [SECURITY.md](SECURITY.md) | [CONTRIBUTING.md](CONTRIBUTING.md) — 14 local Agent Skills (AWS, Azure, GCP, OCI, IBM Bluemix, Alibaba, PCF/Tanzu Well-Architected), zero-trust identity, MCP-Bastion gateway, mcp-test-harness, and AIV PR gate. **No external skill repos.**

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
├── presets/                     # 8 cloud WAF/security presets
├── starter-packs/               # Agent starter YAML bundles
├── examples/mock-posture-check/ # Runnable demo
├── scripts/                     # validate-skills.py, validate-assets.py
├── evals/benchmark/             # Skill routing benchmark
├── registry/                    # assets.json + provenance.yaml
├── LICENSE / VERSION / CHANGELOG.md
└── AGENTS.md                    # Agent routing (read first)
```

Full map: [docs/folder-structure.md](docs/folder-structure.md)

---

## Governance and validation

| Layer | File / command |
|-------|----------------|
| License | [LICENSE](LICENSE) (MIT) |
| Version | [VERSION](VERSION), [CHANGELOG.md](CHANGELOG.md) |
| Skill validator | `python scripts/validate-skills.py` |
| Asset validator | `python scripts/validate-assets.py` |
| Benchmark | `python evals/benchmark/skill_routing_benchmark.py` |
| Provenance | [registry/provenance.yaml](registry/provenance.yaml) |
| Security disclosure | [SECURITY.md](SECURITY.md) |
| Pre-commit | `.pre-commit-config.yaml` |
| Dependabot / CodeQL | `.github/dependabot.yml`, `codeql-analysis.yml` |

---

## Quick demo

```bash
python examples/mock-posture-check/run_posture_check.py
python examples/mock-posture-check/run_posture_check.py --cloud aws --json
```

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
python scripts/validate-skills.py
python scripts/validate-assets.py
python evals/benchmark/skill_routing_benchmark.py
mcp-bastion validate --config bastion.yaml
mcp-test --server-command "python -m agent.mcp_server"
```

Local integration setup: [docs/testing.md](docs/testing.md)

---

## Documentation

| Doc | Topic |
|-----|-------|
| [AGENTS.md](AGENTS.md) | Agent entry + routing |
| [skills-index.md](skills-index.md) | Full skill catalog |
| [docs/folder-structure.md](docs/folder-structure.md) | Directory map |
| [docs/architecture.md](docs/architecture.md) | Threat model |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow |
| [SECURITY.md](SECURITY.md) | Vulnerability disclosure |
| [SUPPORT.md](SUPPORT.md) | Help and contact |

---

## License

MIT
