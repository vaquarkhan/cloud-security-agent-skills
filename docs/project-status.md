# Project status

**Version:** 0.1.0 (initial skeleton)

## Implemented

| Area | Status | Notes |
|------|--------|-------|
| Multi-cloud `IdentityManager` | Done | AWS, Azure, GCP, OCI, IBM, Alibaba, PCF |
| Cloud introspection | Done | Env-signal routing in `security/introspection.py` |
| `DataEngineeringAgent` | Done | Skills load, posture check, Bastion MCP argv |
| Bastion gateway | Done | `bastion.yaml`, proxy, tool wrapper |
| MCP reference server | Done | `plan_pipeline`, `validate_data_contract`, `echo` |
| Skills loader | Done | Core workflow bundle + `SKILLS_PATH` discovery |
| Unit tests | Done | `tests/unit/` — 8 tests |
| MCP integration tests | Done | Protocol + security markers |
| CI workflow | Done | Unit, Bastion validate, harness, AIV gate |
| AIV design rules | Done | No static API keys, no direct MCP bypass |
| Documentation | Done | `docs/`, `AGENTS.md`, folder structure |

## Companion projects (external)

| Project | Role |
|---------|------|
| [MCP-Bastion](https://github.com/vaquarkhan/MCP-Bastion) | PromptGuard, Presidio, rate limits |
| [mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness) | MCP protocol + security tests |
| [aiv-integrity-gate](https://github.com/vaquarkhan/aiv-integrity-gate) | PR logic density + design gates |
| [data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills) | Pipeline workflow skills |

## Planned / not yet in repo

| Item | Priority |
|------|----------|
| `bootstrap.sh` / `bootstrap.ps1` IDE installer | Medium |
| `presets/` multi-cloud DE presets | Medium |
| `examples/` runnable pipeline scaffolds | Medium |
| `hooks/` session guard hooks | Low |
| `registry/assets.json` machine-readable index | Low |
| VS Code / JetBrains plugin surfaces | Low |
| Locked `requirements-lock.txt` | Medium |

## Known limitations

- **PromptGuard model** — requires `transformers` + model weights in production; denylist still blocks common patterns if model unavailable.
- **Presidio cold start** — first PII redaction can take ~60s; CI pre-warms spaCy.
- **Skills not vendored** — clone `data-engineering-agent-skills` separately.

See [architecture.md](architecture.md) for threat model details.
