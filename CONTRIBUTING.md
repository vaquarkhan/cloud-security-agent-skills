# Contributing to cloud-security-agent-skills

Thank you for improving multi-cloud security agent skills and the zero-trust framework.

## Development setup

```bash
git clone git@github.com:vaquarkhan/cloud-security-agent-skills.git
cd cloud-security-agent-skills
pip install -e ".[dev]"
python -m spacy download en_core_web_sm   # for Bastion PII tests
```

## Before opening a PR

```bash
pytest tests/unit/ -v
python scripts/validate-skills.py
python scripts/validate-assets.py
python evals/benchmark/skill_routing_benchmark.py
mcp-bastion validate --config bastion.yaml
pre-commit run --all-files
```

Integration tests (optional locally):

```bash
pip install -e ".[test,bastion]"
mcp-test --transport stdio --server-command "python -m agent.mcp_server" -k protocol
```

See [docs/testing.md](docs/testing.md) for full integration test instructions.

## Skill authoring

- One skill per directory: `skills/<name>/SKILL.md`
- Frontmatter: `name` must match directory; `description` required
- Cloud skills: include verification checklist and red flags
- Add checklist provenance to `registry/provenance.yaml`
- Run `python scripts/validate-skills.py`

## Code standards

- **No static secrets** in code, tests, or examples
- MCP clients must use `agent.bastion_proxy`
- Match existing patterns in `security/` and `agent/`
- Update `CHANGELOG.md` and `VERSION` for notable changes

## Commit messages

Use clear, imperative subjects. Do not include tool/vendor attribution footers.

## Questions

Open a [GitHub Discussion](https://github.com/vaquarkhan/cloud-security-agent-skills/discussions) or see [SUPPORT.md](SUPPORT.md).
