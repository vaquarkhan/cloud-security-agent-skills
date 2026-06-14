# AGENTS.md — Cloud Security Agent Entry Point

Read this before any security work in this repository.

## Mission

Execute **multi-cloud security** assessments and hardening using **local skills only** (`skills/`). Enforce zero-trust identity, MCP-Bastion gateway, mcp-test-harness validation, and AIV PR gates.

**This is a specialized security repo — not data engineering.**

## Mandatory rules

1. **No static secrets** — use `security/IdentityManager` only
2. **MCP via Bastion** — `agent.bastion_proxy`, never raw `agent.mcp_server`
3. **Load cloud skill** matching detected environment
4. **Run validation** before PR: Bastion validate + mcp-test security + AIV

## Skill routing

| Signal | Primary skill |
|--------|---------------|
| Session start | `using-cloud-security-agent-skills` |
| Well-Architected / WAF review (all clouds) | `cloud-well-architected-frameworks` |
| Validate skills / assets | `python scripts/validate-skills.py`, `python scripts/validate-assets.py` |
| Identity / secrets | `zero-trust-identity-and-secrets` |
| AWS | `aws-security-best-practices` |
| Azure | `azure-security-best-practices` |
| GCP | `gcp-security-best-practices` |
| OCI / Oracle | `oci-oracle-cloud-security` |
| IBM Cloud | `ibm-cloud-security-best-practices` |
| Alibaba | `alibaba-cloud-security-best-practices` |
| VMware Tanzu PCF | `vmware-tanzu-pcf-security` |
| Hybrid / unknown cloud | `multi-cloud-security-posture` |
| Bastion / bastion.yaml | `mcp-bastion-security-gateway` |
| MCP tests | `mcp-security-testing-harness` |
| PR quality gate | `pr-integrity-aiv-gate` |

Full catalog: [skills-index.md](skills-index.md)

## Key files

| File | Role |
|------|------|
| `skills/*/SKILL.md` | Security workflows |
| `security/` | Identity managers |
| `bastion.yaml` | Bastion policy |
| `mcp-test.yaml` | Harness config |
| `.aiv/` | AIV gate |
| `.cursorrules` | Bans static keys in AI code |

## Validation

```bash
cloud-security-agent
mcp-bastion validate --config bastion.yaml
pytest tests/unit/ -v
mcp-test-harness stdio --suite security -- python -m agent.mcp_server
```
