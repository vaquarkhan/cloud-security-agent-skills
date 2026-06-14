# Security policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a vulnerability

**Do not** open public GitHub issues for security vulnerabilities.

Report privately to the maintainers:

- **Email:** security@vaquarkhan.dev (or open a private [GitHub Security Advisory](https://github.com/vaquarkhan/cloud-security-agent-skills/security/advisories/new))

Include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment (especially credential exposure, MCP bypass, or Bastion policy gaps)
- Suggested fix if available

## Response timeline

| Stage | Target |
|-------|--------|
| Acknowledgment | 2 business days |
| Initial assessment | 5 business days |
| Fix or mitigation plan | 15 business days (critical: 72 hours) |

## Scope

In scope:

- `security/` IdentityManager credential handling
- `agent/bastion_proxy.py` and `bastion.yaml` policy bypass
- MCP tool handlers that could leak secrets or PII
- AIV design rules gaps allowing static keys in PRs
- Skill content recommending insecure practices (static keys, public data stores)

Out of scope:

- Vulnerabilities in third-party dependencies (report to upstream; we will bump versions)
- Cloud provider platform bugs (report to AWS/Azure/GCP/etc.)
- Issues in consumer MCP clients (Cursor, Claude Desktop) unrelated to this repo

## Safe harbor

We appreciate responsible disclosure. Reporters acting in good faith will not face legal action for discovery activities consistent with this policy.

## Security design principles (this repo)

1. Zero static credentials — workload identity only
2. MCP traffic through Bastion gateway
3. Policy-as-code in `bastion.yaml`
4. PR gates via AIV design rules
5. Adversarial MCP tests in CI

See [docs/architecture.md](docs/architecture.md) for the threat model.
