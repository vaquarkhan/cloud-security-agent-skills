# Folder structure

Canonical map of **cloud-security-agent-skills** — v0.1.0.

---

## Repository tree

```
cloud-security-agent-skills/
├── skills/                         # 14 local security skills (SKILL.md each)
│   ├── using-cloud-security-agent-skills/
│   ├── cloud-well-architected-frameworks/
│   ├── zero-trust-identity-and-secrets/
│   ├── multi-cloud-security-posture/
│   ├── aws-security-best-practices/
│   ├── azure-security-best-practices/
│   ├── gcp-security-best-practices/
│   ├── oci-oracle-cloud-security/
│   ├── ibm-cloud-security-best-practices/
│   ├── alibaba-cloud-security-best-practices/
│   ├── vmware-tanzu-pcf-security/
│   ├── mcp-bastion-security-gateway/
│   ├── mcp-security-testing-harness/
│   └── pr-integrity-aiv-gate/
│
├── security/                       # Zero-trust IdentityManager (7 clouds)
├── agent/                          # CloudSecurityAgent, Bastion, MCP server
├── presets/                        # Per-cloud WAF/security presets (8)
├── starter-packs/                  # YAML starter bundles (4)
├── examples/mock-posture-check/    # Runnable mock posture demo
├── scripts/
│   ├── validate-skills.py          # Skill frontmatter + structure validator
│   └── validate-assets.py          # registry/assets.json path validator
├── evals/benchmark/                # Reproducible skill-routing benchmark
├── registry/
│   ├── assets.json                 # Machine-readable index (schema v2)
│   └── provenance.yaml             # SME source trail for checklists
├── tests/unit/                     # 8 unit tests
├── tests/integration/              # MCP protocol + security tests
├── docs/                           # Architecture, testing, getting started
├── .aiv/                           # AIV PR integrity gate
├── .github/workflows/              # CI, CodeQL
├── .claude/commands/               # Claude Code slash commands
├── .gemini/commands/               # Gemini command surfaces
├── .kiro/steering/                 # Kiro steering rules
├── bastion.yaml                    # MCP-Bastion policy-as-code
├── mcp-test.yaml                   # MCP test harness config
├── LICENSE                         # MIT
├── VERSION                         # Canonical version (0.1.0)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── SUPPORT.md
├── CLAUDE.md                       # Claude Code entry
├── AGENTS.md                       # Agent routing (read first)
├── skills-index.md
├── requirements-lock.txt
└── .pre-commit-config.yaml
```

---

## Module responsibilities

| Path | Responsibility |
|------|----------------|
| `security/` | Ephemeral credential lifecycle — **no static API keys** |
| `agent/orchestrator.py` | Cloud introspection, skill load, posture pre-flight |
| `agent/bastion_proxy.py` | Stdio MCP proxy — security gateway hop |
| `agent/skills_loader.py` | Local `skills/` discovery and core bundle |
| `scripts/validate-skills.py` | CI skill validator |
| `registry/assets.json` | Paths, presets, examples, install surfaces |
| `registry/provenance.yaml` | Checklist SME provenance |

---

## Entry points

| Command | Purpose |
|---------|---------|
| `cloud-security-agent` | Posture check + Bastion MCP argv |
| `python examples/mock-posture-check/run_posture_check.py` | Mock multi-cloud demo |
| `python scripts/validate-skills.py` | Validate all SKILL.md files |
| `python evals/benchmark/skill_routing_benchmark.py` | Skill routing score |

---

## Related docs

| Doc | Topic |
|-----|-------|
| [architecture.md](architecture.md) | Threat model |
| [testing.md](testing.md) | Local + CI test commands |
| [project-status.md](project-status.md) | Feature list |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Development workflow |
| [../SECURITY.md](../SECURITY.md) | Vulnerability disclosure |
