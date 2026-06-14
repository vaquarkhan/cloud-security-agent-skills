# Support

## Documentation

| Resource | Description |
|----------|-------------|
| [README.md](README.md) | Overview and quick start |
| [AGENTS.md](AGENTS.md) | Agent routing entry point |
| [skills-index.md](skills-index.md) | Full skill catalog |
| [docs/getting-started.md](docs/getting-started.md) | Bootstrap and IDE setup |
| [docs/testing.md](docs/testing.md) | Unit and integration tests |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development workflow |

## Getting help

- **Bug reports / features:** [GitHub Issues](https://github.com/vaquarkhan/cloud-security-agent-skills/issues)
- **Questions / architecture:** [GitHub Discussions](https://github.com/vaquarkhan/cloud-security-agent-skills/discussions)
- **Security vulnerabilities:** [SECURITY.md](SECURITY.md) — do not use public issues

## Quick commands

```bash
cloud-security-agent                              # posture check
python examples/mock-posture-check/run_posture_check.py  # mock demo
python scripts/validate-skills.py                 # validate all skills
mcp-bastion validate --config bastion.yaml        # Bastion policy
```

## Companion projects

| Project | Role |
|---------|------|
| [MCP-Bastion](https://github.com/vaquarkhan/MCP-Bastion) | Security gateway |
| [mcp-test-harness](https://github.com/vaquarkhan/mcp-test-harness) | MCP test suite |
| [aiv-integrity-gate](https://github.com/vaquarkhan/aiv-integrity-gate) | PR integrity gate |

## Commercial / enterprise

For enterprise deployment reviews (multi-cloud WAF workshops, Bastion hardening, agent identity architecture), contact the maintainer via GitHub Discussions or project email listed in repository metadata.
