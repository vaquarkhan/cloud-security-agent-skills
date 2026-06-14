---
preset_id: aws-security
name: AWS Security
version: "1.0.0"
cloud_provider: aws
frameworks:
  - AWS-Well-Architected-Security
  - CIS-AWS-Foundations-v3
skills:
  - aws-security-best-practices
  - zero-trust-identity-and-secrets
  - cloud-well-architected-frameworks
---

# AWS Security Preset

End-to-end AWS hardening for agents and workloads. **No static access keys.**

## Load order

1. `zero-trust-identity-and-secrets`
2. `aws-security-best-practices`
3. `mcp-bastion-security-gateway`

## Identity (agents)

- IAM Identity Center for humans
- **IRSA** / instance profile for agents — `AWSCredentialChainManager`

## Priority controls

| Area | Services |
|------|----------|
| Governance | Organizations, SCPs, Control Tower |
| IAM | SSO, permission boundaries, Access Analyzer |
| Encryption | KMS, Secrets Manager, SSE-KMS on S3/RDS |
| Network | VPC, WAF, VPC endpoints, Flow Logs |
| Detection | CloudTrail org, GuardDuty, Security Hub |

## Checklist

`skills/aws-security-best-practices/references/end-to-end-checklist.md`

## MCP

```json
{"command": "python", "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]}
```
