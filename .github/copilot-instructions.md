# GitHub Copilot instructions — cloud-security-agent-skills

You are assisting with **multi-cloud zero-trust security** work in this repository.

## Mandatory rules

1. **No static secrets** — use `security/IdentityManager`; never hard-code `AKIA*`, `client_secret`, AccessKeys, or API signing keys
2. **MCP via Bastion** — clients must use `agent.bastion_proxy`, not raw `agent.mcp_server`
3. **Load the matching cloud skill** before AWS/Azure/GCP/OCI/IBM/Alibaba/PCF security work
4. **Well-Architected reviews** — use `cloud-well-architected-frameworks` for cross-cloud WAF pillars

## Skill routing

- Session start → `using-cloud-security-agent-skills`
- Identity → `zero-trust-identity-and-secrets`
- WAF / architecture → `cloud-well-architected-frameworks`
- Hybrid → `multi-cloud-security-posture` + per-cloud skills

## Security lifecycle

`/assess` → `/harden` → `/validate` (mcp-test) → `/gate` (AIV)

## Before suggesting commits

- Run `python scripts/validate-skills.py`
- No tool/vendor attribution in commit messages
- See `SECURITY.md` for vulnerability disclosure

Read [AGENTS.md](../AGENTS.md) for full routing.
