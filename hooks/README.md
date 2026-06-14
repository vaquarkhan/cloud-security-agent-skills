# Session hooks — cloud-security-agent-skills

Optional hooks for agent sessions (Cursor / compatible IDEs).

| Hook | Purpose |
|------|---------|
| `session-start.sh` / `.ps1` | Print posture reminder — zero-trust, Bastion, skill routing |
| `no-static-secrets-guard.sh` / `.ps1` | Scan staged diff for static key patterns (pre-commit companion) |

Install via `./bootstrap.sh --target hooks` or IDE plugin **Install Full Toolkit**.
