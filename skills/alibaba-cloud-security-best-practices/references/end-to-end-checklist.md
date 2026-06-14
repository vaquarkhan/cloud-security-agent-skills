# Alibaba Cloud End-to-End Security Checklist

Use with `alibaba-cloud-security-best-practices` skill.

## Governance
- [ ] Resource Directory multi-account
- [ ] Control policies (deny public OSS, restrict AccessKey)
- [ ] Resource groups and tags per app/env
- [ ] Cloud Config org rules

## RAM & Identity
- [ ] MFA on all RAM users
- [ ] ECS instance RAM role / RRSA for workloads
- [ ] No AccessKey in code, CI, or containers
- [ ] STS AssumeRole with external ID for third parties
- [ ] Permission boundaries on automation roles

## KMS & Secrets
- [ ] HSM CMK for prod
- [ ] OSS/RDS/disk encryption with KMS
- [ ] Secrets Manager rotation

## Network
- [ ] VPC segmentation; private RDS/ECS
- [ ] Security groups least privilege
- [ ] VPC Flow Logs
- [ ] Cloud Firewall + WAF on public entry
- [ ] PrivateLink for OSS/KMS

## ACK
- [ ] Private cluster API
- [ ] RRSA for pods
- [ ] ACR image scan

## Logging & Detection
- [ ] ActionTrail org-wide to Log Archive
- [ ] Security Center all modules
- [ ] Alerts on CreateAccessKey, public bucket policy

## Agent / MCP
- [ ] EcsRamRoleCredentialProvider pattern
- [ ] Bastion MCP proxy
