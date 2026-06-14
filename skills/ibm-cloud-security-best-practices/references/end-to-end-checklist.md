# IBM Cloud End-to-End Security Checklist

Use with `ibm-cloud-security-best-practices` skill.

## Governance
- [ ] Enterprise/account groups (prod, nonprod, security)
- [ ] Resource groups per app/env
- [ ] Tags: env, data_class, owner
- [ ] MFA account setting enforced

## IAM
- [ ] Access groups (not ad-hoc user policies)
- [ ] Trusted Profile for compute — no API keys on workloads
- [ ] Service IDs scoped via access groups
- [ ] Dynamic rules from corporate IdP

## Key Protect & Secrets
- [ ] HPCS/Key Protect for prod CMK
- [ ] Dual authorization on key delete
- [ ] Secrets Manager rotation where supported
- [ ] COS encryption with KP/HPCS

## Network
- [ ] VPC Gen2 security groups default deny
- [ ] Private Path for IBM services
- [ ] CIS WAF on public apps
- [ ] No public DB endpoints

## Compute & IKS
- [ ] IKS private endpoint
- [ ] Trusted Profile on workers/pods
- [ ] Vulnerability Advisor on images/VSIs

## Logging & Detection
- [ ] Activity Tracker to immutable COS
- [ ] SCC profiles enabled with remediation owners
- [ ] Alerts on API key create, policy change

## Agent / MCP
- [ ] TRUSTED_PROFILE_NAME only
- [ ] Bastion proxy; AIV on PRs
