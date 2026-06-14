# Testing

Test layout and commands for **cloud-security-agent-skills**.

## Layout

```
tests/
├── unit/                           # Plain pytest — no MCP subprocess
│   └── test_identity_and_gateway.py
└── integration/                    # mcp-test-harness fixtures (mcp_server)
    └── test_mcp_integration.py
        @pytest.mark.protocol       # MCP handshake, tools, resources
        @pytest.mark.security       # Bastion adversarial + PII (requires mcp-bastion)
```

Config: [`mcp-test.yaml`](../mcp-test.yaml) — server command, `tests/integration/`, 120s timeout.

## Commands

```bash
# Unit tests
pytest tests/unit/ -v

# All MCP integration tests
mcp-test --transport stdio --server-command "python -m agent.mcp_server"

# Protocol conformance only
mcp-test --transport stdio --server-command "python -m agent.mcp_server" -k protocol

# Security suite (documented CLI form)
mcp-test-harness stdio --suite security -- python -m agent.mcp_server
```

## Security test expectations

| Test | Asserts |
|------|---------|
| `test_bastion_blocks_prompt_injection` | Adversarial prompt blocked or sanitized |
| `test_bastion_redacts_pii` | SSN/email not echoed raw in tool output |
| `test_output_leak_scanner_no_api_key_pattern` | `api_key=sk-live-...` blocked or stripped |

Security tests call `pytest.importorskip("mcp_bastion")` — install with `pip install -e ".[bastion]"`.

## CI

See [`.github/workflows/ci.yml`](../.github/workflows/ci.yml):

1. `pytest tests/unit/`
2. `mcp-bastion validate --config bastion.yaml`
3. `mcp-test` protocol + security harness
4. AIV gate on pull requests

## Presidio warm-up

First Presidio call loads spaCy (~60s). CI runs:

```bash
python -m spacy download en_core_web_sm
python -c "from mcp_bastion.pillars.pii_redaction import PIIRedactor; PIIRedactor().redact_text('warmup')"
```
