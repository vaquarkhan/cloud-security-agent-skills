# Project status

**Version:** 0.1.0 — see [VERSION](../VERSION) and [CHANGELOG](../CHANGELOG.md)

## Implemented

| Area | Status | Notes |
|------|--------|-------|
| Multi-cloud `IdentityManager` | Done | AWS, Azure, GCP, OCI, IBM, Alibaba, PCF |
| Cloud introspection | Done | Env-signal routing in `security/introspection.py` |
| `CloudSecurityAgent` | Done | Skills load, posture check, Bastion MCP argv |
| Bastion gateway | Done | `bastion.yaml`, proxy, tool wrapper |
| MCP reference server | Done | Security tools: posture, controls, echo |
| **14 security skills** | Done | End-to-end per cloud + WAF + zero-trust |
| Skills loader | Done | Local `skills/` only |
| Unit tests | Done | `tests/unit/` — 8 tests |
| MCP integration tests | Done | Protocol + security markers |
| CI workflow | Done | Validate skills/assets, benchmark, unit, Bastion, harness, AIV |
| AIV design rules | Done | No static API keys, no direct MCP bypass |
| **LICENSE (MIT)** | Done | `LICENSE` |
| **CHANGELOG / VERSION** | Done | Semantic versioning |
| **validate-skills.py** | Done | Frontmatter, structure, registry |
| **validate-assets.py** | Done | Path validation for `registry/assets.json` |
| **Governance docs** | Done | CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, SUPPORT |
| **Presets / starter-packs** | Done | 8 presets, 4 starter packs |
| **Runnable example** | Done | `examples/mock-posture-check/` |
| **Multi-IDE surfaces** | Done | CLAUDE.md, `.claude/`, `.gemini/`, `.kiro/` |
| **Provenance trail** | Done | `registry/provenance.yaml` |
| **Eval benchmark** | Done | `evals/benchmark/skill_routing_benchmark.py` |
| **Dependabot / CodeQL / pre-commit** | Done | Governance layers |
| **requirements-lock.txt** | Done | Pinned core dependencies |
| Documentation | Done | `docs/`, `AGENTS.md`, folder structure |

## Companion projects (external)

| Project | Role |
|---------|------|
| [MCP-Bastion](https://github.com/vaquarkhan/MCP-Bastion) | PromptGuard, Presidio, rate limits |
| [mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness) | MCP protocol + security tests |
| [aiv-integrity-gate](https://github.com/vaquarkhan/aiv-integrity-gate) | PR logic density + design gates |

## Known limitations

- **PromptGuard model** — requires `transformers` + model weights in production; denylist still blocks common patterns if model unavailable.
- **Presidio cold start** — first PII redaction can take ~60s; CI pre-warms spaCy.
- **Integration tests** — require `pip install -e ".[test,bastion]"` locally; see [testing.md](testing.md).

See [architecture.md](architecture.md) for threat model details.
