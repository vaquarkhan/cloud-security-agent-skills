---
name: mcp-security-testing-harness
description: End-to-end MCP security testing — mcp-test-harness protocol conformance, adversarial injection, PII leak detection, API key pattern checks, CI integration against agent.mcp_server via Bastion.
---

# MCP Security Testing Harness (End-to-End)

## Overview

Automated **adversarial and protocol testing** for MCP servers using [mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness). Validates that Bastion + MCP handlers resist injection, do not leak PII or secrets, and conform to JSON-RPC MCP schema.

Config: **`mcp-test.yaml`** at repo root.

---

## 1. Test pyramid

| Layer | Location | Markers |
|-------|----------|---------|
| Unit | `tests/unit/` | Fast, no MCP transport |
| Integration protocol | `tests/integration/test_mcp_integration.py` | `@pytest.mark.protocol` |
| Integration security | same file | `@pytest.mark.security` |
| Harness CLI | `mcp-test` / `mcp-test-harness` | Full suite via YAML |

---

## 2. Commands

```bash
# Full harness (stdio transport)
mcp-test --transport stdio --server-command "python -m agent.mcp_server"

# Protocol conformance only
mcp-test --transport stdio --server-command "python -m agent.mcp_server" -k protocol

# Security suite (adversarial + PII)
mcp-test-harness stdio --suite security -- python -m agent.mcp_server

# Pytest integration
pytest tests/integration/ -m security
pytest tests/integration/ -m protocol
```

### Testing through Bastion (recommended for prod parity)

```bash
mcp-test --transport stdio --server-command "python -m agent.bastion_proxy -- python -m agent.mcp_server"
```

---

## 3. Security test categories

### Protocol (`@pytest.mark.protocol`)

- MCP handshake and initialize
- `tools/list` schema
- `tools/call` request/response shape
- Error handling for malformed JSON-RPC

### Security (`@pytest.mark.security`)

| Test intent | Pass criteria |
|-------------|---------------|
| Prompt injection in tool args | Blocked or sanitized; no instruction override in output |
| PII in tool input (SSN, email) | Redacted in response (Presidio via Bastion when proxied) |
| API key patterns in mock data | Not echoed raw (`AKIA`, `sk-`, etc.) |
| Oversized payloads | Rejected or truncated per rate limits |
| Tool not in RBAC | Denied when RBAC enforced |

---

## 4. `mcp-test.yaml` configuration

Key settings in repo root:

- `transport: stdio`
- `server_command` — points to MCP server (or Bastion-wrapped)
- `timeout` — increased for Presidio cold start (120s in CI)
- `schema_validation` — MCP schema checks at root level

Review `mcp-test.yaml` when adding new tools.

---

## 5. CI pipeline (`.github/workflows/ci.yml`)

Typical order:

1. Unit tests (`pytest tests/unit/`)
2. `mcp-bastion validate`
3. Pre-warm Presidio/spaCy models (avoid PII test timeout)
4. `mcp-test` integration suite
5. AIV gate on PRs

**PR requirement:** security suite green before merge.

---

## 6. Adding tests for new MCP tools

When adding a tool to `agent/mcp_server/`:

1. Add protocol test — list + call happy path
2. Add security test — injection string in each string argument
3. Add PII test if tool returns user-provided text
4. Update `bastion.yaml` RBAC if new tool name
5. Run full suite locally

---

## 7. Failure triage

| Failure | Likely cause |
|---------|--------------|
| PII test timeout | Presidio model not downloaded; increase timeout |
| Injection test fail | PromptGuard pattern gap — update `bastion.yaml` |
| Schema validation | MCP SDK version drift — update tool schemas |
| RBAC deny | Tool not in allowlist — intentional or fix rbac |

---

## 8. Verification checklist

- [ ] `pytest tests/unit/` green
- [ ] Protocol tests green
- [ ] Security tests green (local + CI)
- [ ] Tested with Bastion proxy for prod-like path
- [ ] New tools have security coverage
- [ ] PII tests pass within CI timeout

---

## 9. Red flags

- Security tests skipped in CI (`-k "not security"`)
- Only testing raw server without Bastion in prod config
- No adversarial cases for new string parameters
- Disabling schema validation to "fix" CI

---

## Related skills

- `mcp-bastion-security-gateway`
- `pr-integrity-aiv-gate`
- `using-cloud-security-agent-skills`
