---
name: pr-integrity-aiv-gate
description: End-to-end AIV PR integrity gate — logic density, YAML design rules, forbidden API keys and MCP bypass patterns, dependency and invariant checks before human review.
---

# PR Integrity — AIV Gate (End-to-End)

## Overview

**AIV (Automated Integrity Validation)** blocks low-quality, unsafe, or AI-slop PRs before human review. Maven artifact: `io.github.vaquarkhan:aiv-gate`. Config: **`.aiv/config.yaml`** and **`.aiv/design-rules.yaml`**.

Mandatory for this repo's CI on every pull request.

---

## 1. Gate architecture

```
PR opened/updated
    ↓
git diff vs base branch
    ↓
AIV CLI (density + design + dependency + invariant)
    ↓
PASS → human review allowed
FAIL → fix violations or reject PR
```

---

## 2. Gate types

| Gate | Purpose | Examples in this repo |
|------|---------|----------------------|
| **density** | Logic density, entropy — flags boilerplate/slop | Oversized generated files with low unique logic |
| **design** | Forbidden patterns in diff | Static API keys, MCP bypass, hardcoded secrets |
| **dependency** | Import/supply-chain risks | Unexpected new deps, known bad versions |
| **invariant** | Property-based hooks | Security invariants from `.aiv/invariants/` |

---

## 3. Design rules (this repo)

Enforced via `.aiv/design-rules.yaml`:

| Rule | Rationale |
|------|-----------|
| No `os.getenv("API_KEY")` with static defaults | Prevents baked-in secrets |
| No `aws_access_key_id=` in code | AWS static key ban |
| No `client_secret=` literals | Azure secret ban |
| No direct `agent.mcp_server` in MCP configs | Bastion bypass |
| No `.env` committed with secrets | Git leak prevention |
| No `password=` / `token=` literals in Python values | Generic secret ban |

Aligns with `zero-trust-identity-and-secrets` and `.cursorrules`.

---

## 4. CI integration

`.github/workflows/ci.yml` on pull requests:

```bash
java -jar aiv-cli.jar --workspace . --diff origin/main ...
```

Or composite action: `vaquarkhan/aiv-integrity-gate@v1`

**Merge policy:** AIV PASS required alongside:

- Unit tests
- Bastion validate
- mcp-test security suite

---

## 5. Local usage

1. Download AIV CLI from Maven Central (see CI workflow for version pin)
2. Run against working tree:

```bash
java -jar aiv-cli.jar --workspace . --diff origin/main
```

3. Fix reported design rule paths — **do not suppress** without security review

---

## 6. Workflow for agents and developers

1. Make changes following cloud security skills
2. Run `pytest tests/unit/` locally
3. Run AIV locally before push
4. Open PR — CI re-runs full stack
5. Address AIV FAIL with minimal fix (not rule disable)

---

## 7. Common violations and fixes

| Violation | Fix |
|-----------|-----|
| AKIA in test fixture | Use mock ARN or `AKIA...` redacted placeholder marked safe in test-only file with review |
| MCP config without proxy | Add `agent.bastion_proxy` wrapper |
| New env var with default secret | Remove default; use vault at runtime |
| Low density huge file | Split or replace boilerplate with focused logic |

---

## 8. Verification checklist

- [ ] AIV PASS on PR before merge
- [ ] No design rule suppressions without ticket
- [ ] `.aiv/design-rules.yaml` updated when new anti-patterns discovered
- [ ] CI runs AIV on all PR targets (main/master)
- [ ] Aligns with `.cursorrules` static secret ban

---

## 9. Red flags

- `--skip-design` or equivalent in CI
- Blanket suppressions for `aws_access_key_id`
- Merging with AIV FAIL "to unblock"
- AIV not run on agent-generated bulk commits

---

## Related skills

- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `mcp-security-testing-harness`
- `using-cloud-security-agent-skills`
