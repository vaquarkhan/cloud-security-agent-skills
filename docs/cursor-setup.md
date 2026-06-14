# Cursor setup

Install **cloud-security-agent-skills** for Cursor.

## Bootstrap (recommended)

```bash
./bootstrap.sh --target cursor
# or full install:
./bootstrap.sh
```

Installs:

- `.cursor/rules/` — zero-trust, Bastion, cloud WAF routing
- `skills/` — 14 security skills (via core pack when using full bootstrap)
- `AGENTS.md`, `skills-index.md`

## Manual

1. Clone this repo or open as workspace
2. Point Cursor **Agent Skills** at `./skills/`
3. Ensure MCP uses Bastion — see [bastion-policy.md](bastion-policy.md)

## Rules installed

| Rule | Purpose |
|------|---------|
| `00-cloud-security-core.mdc` | Security-only repo, validators |
| `10-zero-trust-identity.mdc` | IdentityManager, no static keys |
| `20-bastion-gateway-required.mdc` | MCP proxy mandatory |
| `30-cloud-waf-routing.mdc` | Per-cloud skill routing |

## MCP

```json
{
  "command": "python",
  "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]
}
```

## Validate

```bash
cloud-security-agent
python scripts/validate-skills.py
```
