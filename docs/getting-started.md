# Getting started

## Install

```bash
git clone git@github.com:vaquarkhan/cloud-security-agent-skills.git
cd cloud-security-agent-skills
./bootstrap.sh    # Windows: .\bootstrap.ps1
```

## Verify skills (all local)

```bash
cloud-security-agent
```

Expect `skills_complete: true` and `available_count: 14`.

## MCP client

```json
{
  "command": "python",
  "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]
}
```

## Load skills in Cursor

Point Cursor skills at `./skills/` — all 14 security skills are in this repo.

Start with `using-cloud-security-agent-skills`, then the cloud skill for your environment.

## Test

```bash
pytest tests/unit/ -v
mcp-test-harness stdio --suite security -- python -m agent.mcp_server
```
