# Folder structure

Canonical map of **cloud-security-agent-skills** — what each directory and key file is for. Use this when onboarding, extending the agent, or wiring CI.

---

## Repository tree

```
cloud-security-agent-skills/
├── agent/                          # Data Engineering Agent core + MCP surfaces
│   ├── __init__.py                 # Public exports: BastionGateway, DataEngineeringAgent
│   ├── orchestrator.py             # DataEngineeringAgent — introspection, skills, posture
│   ├── bastion_gateway.py          # BastionGateway — policy load, MCP launch argv
│   ├── bastion_proxy.py            # Stdio MCP proxy (agent → Bastion → upstream server)
│   ├── bastion_wrapper.py          # In-process Bastion checks on FastMCP tool handlers
│   ├── skills_loader.py            # Loads workflow skills from data-engineering-agent-skills
│   ├── harness_cli.py              # mcp-test-harness CLI shim (stdio --suite security)
│   └── mcp_server/                 # Bastion-protected MCP tool server (STDIO)
│       ├── __init__.py
│       └── __main__.py             # echo, plan_pipeline, validate_data_contract tools
│
├── security/                       # Zero-trust multi-cloud identity abstraction
│   ├── __init__.py                 # CloudCredentials, detect_cloud_environment, get_identity_manager
│   ├── base.py                     # IdentityManager ABC + token lifecycle
│   ├── introspection.py            # CloudEnvironment detection + manager routing
│   ├── aws.py                      # AWSCredentialChainManager (boto3 default chain)
│   ├── azure.py                    # AzureDefaultCredentialManager
│   ├── gcp.py                      # GCPDefaultCredentialManager (ADC)
│   ├── oci.py                      # OCIResourcePrincipalManager + Vault client
│   ├── ibm.py                      # IBMTrustedProfileManager (TRUSTED_PROFILE_NAME)
│   ├── alibaba.py                  # AlibabaRAMRoleManager (ram_role_arn STS refresh)
│   └── pcf.py                      # PCFCredHubManager (VCAP_SERVICES / UAA OAuth2)
│
├── tests/
│   ├── unit/                       # Fast pytest — no MCP subprocess, no cloud SDKs
│   │   └── test_identity_and_gateway.py
│   └── integration/                # mcp-test-harness — STDIO MCP server tests
│       └── test_mcp_integration.py # @pytest.mark.protocol | @pytest.mark.security
│
├── docs/                           # Setup, architecture, and structure guides
│   ├── folder-structure.md         # This file
│   ├── architecture.md             # Threat model + data flow
│   ├── getting-started.md          # First-run walkthrough
│   ├── project-status.md           # Feature list and roadmap
│   ├── identity-layer.md           # Per-cloud IdentityManager reference
│   ├── bastion-policy.md           # bastion.yaml tuning guide
│   └── testing.md                  # mcp-test-harness + CI commands
│
├── .aiv/                           # AIV integrity gate (PR validation)
│   ├── config.yaml                 # Density, design, dependency, invariant gates
│   └── design-rules.yaml         # Forbidden patterns (API keys, direct MCP bypass)
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # Unit, Bastion validate, MCP harness, AIV gate
│
├── bastion.yaml                    # MCP-Bastion policy-as-code (PromptGuard, PII, rate limits)
├── mcp-test.yaml                   # mcp-test-harness config (server command, timeouts)
├── pyproject.toml                  # Package metadata, extras, pytest markers, entry points
├── requirements.txt                # Pinned runtime + test + cloud SDK deps
├── .cursorrules                    # Cursor AI rules — bans static secrets in generated code
├── .env.example                    # Safe env var template (no real values)
├── AGENTS.md                       # Agent entry + skill routing (read first)
└── README.md                       # Project overview + quick links
```

---

## Module responsibilities

| Path | Responsibility |
|------|----------------|
| `security/` | Autonomous short-lived credential lifecycle; **no static API keys** |
| `agent/orchestrator.py` | Cloud introspection, skill bundle load, security posture pre-flight |
| `agent/bastion_gateway.py` | Single entry for Bastion policy; agents **must not** bypass this |
| `agent/bastion_proxy.py` | Process-level stdio proxy between IDE/agent and upstream MCP |
| `agent/bastion_wrapper.py` | Tool-level inbound (injection, denylist) + outbound (Presidio) checks |
| `agent/skills_loader.py` | Progressive load of `data-engineering-agent-skills` workflows |
| `agent/mcp_server/` | Reference MCP server for pipeline plan / contract validation tools |
| `bastion.yaml` | Production security posture — review PII entities before deploy |
| `tests/unit/` | Identity routing, gateway argv, skills stubs |
| `tests/integration/` | MCP protocol conformance + adversarial/PII security suite |
| `.aiv/` | PR gate — logic density, YAML design rules, invariants |

---

## External skill dependency

Workflow skills are **not vendored** in this repo. Clone separately and point `SKILLS_PATH`:

```
vendor/data-engineering-agent-skills/
└── skills/
    ├── using-data-engineering-agent-skills/
    ├── data-specification/
    ├── pipeline-planning-and-task-breakdown/
    ├── python-data-engineering-and-pipeline-packaging/
    ├── data-quality-and-contract-testing/
    ├── orchestration-and-backfills/
    └── lineage-pii-and-governance/
```

See [data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills).

---

## Entry points (CLI)

| Command | Module | Purpose |
|---------|--------|---------|
| `cloud-de-agent` | `agent.orchestrator:main` | Print security posture + Bastion-wrapped MCP argv |
| `python -m agent.bastion_proxy` | `agent/bastion_proxy.py` | Stdio proxy with `--` upstream command |
| `python -m agent.mcp_server` | `agent/mcp_server/__main__.py` | Bastion-wrapped MCP tool server |
| `mcp-test-harness stdio --suite security -- python -m agent.mcp_server` | `agent/harness_cli.py` | Security integration test suite |

---

## Config files

| File | Loaded by | Purpose |
|------|-----------|---------|
| `bastion.yaml` | `BastionGateway`, `bastion_wrapper`, `mcp-bastion validate` | PromptGuard, Presidio, rate limit, RBAC, cost |
| `mcp-test.yaml` | `mcp-test` / `mcp-test-harness` | Server command, test dirs, schema validation |
| `.aiv/config.yaml` | AIV CLI on PR | Logic density + design compliance |
| `.env` (local only) | Runtime | `SKILLS_PATH`, `BASTION_CONFIG`, alert webhooks |

---

## Related docs

| Doc | Topic |
|-----|-------|
| [architecture.md](architecture.md) | End-to-end data flow and threat model |
| [getting-started.md](getting-started.md) | Bootstrap and first MCP connection |
| [identity-layer.md](identity-layer.md) | Per-cloud identity managers |
| [bastion-policy.md](bastion-policy.md) | `bastion.yaml` compliance tuning |
| [testing.md](testing.md) | Unit + MCP harness commands |
| [project-status.md](project-status.md) | Implemented vs planned |
| [../AGENTS.md](../AGENTS.md) | Agent routing rules |
