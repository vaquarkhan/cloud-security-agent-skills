# cloud-security-agent-skills — Claude Code entry

Read [AGENTS.md](AGENTS.md) first. This repo is a **security-only** multi-cloud agent framework.

## Rules

1. **No static secrets** — use `security/IdentityManager`
2. **MCP via Bastion** — never raw `agent.mcp_server`
3. Load **`cloud-well-architected-frameworks`** for WAF reviews
4. Load matching cloud skill (AWS, Azure, GCP, OCI, IBM/Bluemix, Alibaba, PCF/Tanzu)

## Commands

- `/posture-check` — run agent posture validation
- `/aws-security-review` — AWS end-to-end security assessment

## Key paths

- Skills: `skills/`
- Bastion: `bastion.yaml`
- Presets: `presets/`
- Example: `examples/mock-posture-check/run_posture_check.py`
