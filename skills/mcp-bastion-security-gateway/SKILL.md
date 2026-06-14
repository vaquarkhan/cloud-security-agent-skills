---
name: mcp-bastion-security-gateway
description: End-to-end MCP-Bastion — PromptGuard injection defense, Presidio PII redaction, rate limits, cycle detection, RBAC, content filter, audit, cost caps. All MCP clients must use agent.bastion_proxy.
---

# MCP Bastion Security Gateway (End-to-End)

## Overview

**MCP-Bastion** is the mandatory security gateway between LLM clients and MCP tool servers. No agent in this repo may expose raw `agent.mcp_server` to clients. Policy: **`bastion.yaml`** at repo root.

---

## 1. Architecture

```
LLM Client (Cursor, etc.)
    ↓ stdio
agent.bastion_proxy          ← policy enforcement hop
    ↓ stdio
agent.mcp_server             ← tools: assess_cloud_posture, etc.
    ↓
Cloud APIs (via IdentityManager — no static keys)
```

Components in this repo:

| File | Role |
|------|------|
| `bastion.yaml` | Policy pillars (single source of truth) |
| `agent/bastion_gateway.py` | Load policy, produce launch argv |
| `agent/bastion_proxy.py` | Stdio proxy — inspect/redact/block |
| `agent/bastion_wrapper.py` | `@bastion_tool` decorators on handlers |
| `docs/bastion-policy.md` | Operator tuning guide |

---

## 2. Policy pillars (`bastion.yaml`)

| Pillar | Purpose | Key controls |
|--------|---------|--------------|
| **prompt_guard** | Meta PromptGuard — block jailbreaks, instruction override in tool args | Block patterns, max arg length |
| **pii** | Microsoft Presidio — redact SSN, email, phone, credit card before LLM | Entity list, confidence threshold |
| **rate_limit** | Abuse prevention | Token budget, max iterations, cycle detection |
| **content_filter** | Denylist secrets and injection in responses | API key regex, `password=`, AWS AKIA patterns |
| **rbac** | Tool allowlists by role | `echo_security_context`, `assess_cloud_posture`, `validate_security_controls` |
| **cost_tracker** | FinOps caps | Per-session/day limits |
| **audit** | Request audit trail | Log tool name, duration, filter hits (no secrets) |

Validate locally and in CI:

```bash
mcp-bastion validate --config bastion.yaml
```

---

## 3. MCP client configuration (required)

### Cursor / Claude Desktop / any stdio MCP client

```json
{
  "mcpServers": {
    "cloud-security-agent": {
      "command": "python",
      "args": [
        "-m", "agent.bastion_proxy", "--",
        "python", "-m", "agent.mcp_server"
      ],
      "cwd": "/path/to/cloud-security-agent-skills"
    }
  }
}
```

**Wrong** (never use):

```json
"args": ["-m", "agent.mcp_server"]
```

---

## 4. Threat model coverage

| Threat | Bastion control |
|--------|-----------------|
| Prompt injection via tool args | PromptGuard |
| PII leak to LLM context | Presidio redaction |
| Secret echo in tool output | Content filter |
| Runaway agent loops | Rate limit + cycle detection |
| Unauthorized tool invocation | RBAC allowlist |
| Cost abuse | Cost tracker |
| Forensics gap | Audit pillar |

---

## 5. Integration with cloud security skills

- Agents call cloud APIs **after** identity layer (`IdentityManager`) — Bastion does not replace IAM
- Bastion ensures **cloud credentials never appear** in MCP messages
- Pair with `mcp-security-testing-harness` — security suite asserts PII/key patterns blocked

---

## 6. Compliance tuning

Before production:

1. Review `pii.entities` with legal/privacy — add national IDs if required
2. Review `content_filter.denylist_patterns` with security — add internal secret formats
3. Set `rate_limit` appropriate to workload (batch vs interactive)
4. Enable audit export to SIEM if Bastion supports sink in your deployment
5. Document in `docs/bastion-policy.md`

---

## 7. CI/CD

`.github/workflows/ci.yml`:

1. `mcp-bastion validate --config bastion.yaml`
2. `mcp-test` integration tests (PII, injection)
3. AIV design rule: no MCP bypass

---

## 8. Verification checklist

- [ ] All MCP configs use `agent.bastion_proxy`
- [ ] `mcp-bastion validate` passes locally and in CI
- [ ] RBAC lists only required tools
- [ ] Presidio models warmed in CI (spaCy)
- [ ] Content filter includes cloud key patterns (AKIA, etc.)
- [ ] Audit enabled; no secrets in audit logs
- [ ] AIV design rules forbid direct MCP connection

---

## 9. Red flags

- "Temporary" direct MCP connection left in prod config
- PII entities list empty for regulated data
- Rate limits disabled for "performance"
- Tool allowlist includes unimplemented/high-risk tools

---

## Related skills

- `mcp-security-testing-harness`
- `zero-trust-identity-and-secrets`
- `pr-integrity-aiv-gate`
