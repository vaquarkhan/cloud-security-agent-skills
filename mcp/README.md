# MCP templates — cloud-security-agent-skills

Pre-configured MCP client templates for **Bastion-protected** cloud security tools.

## Bastion Gateway (required)

| File | Purpose |
|------|---------|
| [cloud-security-agent.mcp.json](cloud-security-agent.mcp.json) | Stdio MCP via `agent.bastion_proxy` |
| [../templates/bastion-mcp-client.json](../templates/bastion-mcp-client.json) | Copy-paste template for Cursor/Claude |

## Tools exposed (via Bastion)

- `echo_security_context` — integration test echo (PII redacted)
- `assess_cloud_posture` — route to cloud security skill
- `validate_security_controls` — framework validation stub

## Install

**VS Code / Cursor:** Command palette → `Cloud Security Agent Skills: Install MCP Bastion Templates`

**JetBrains:** Tools → Cloud Security Agent Skills → Install MCP Bastion Templates

**CLI:**

```bash
./bootstrap.sh --target mcp
```

## Policy

All traffic governed by [`bastion.yaml`](../bastion.yaml) — validate with:

```bash
mcp-bastion validate --config bastion.yaml
```

See skill `mcp-bastion-security-gateway`.
