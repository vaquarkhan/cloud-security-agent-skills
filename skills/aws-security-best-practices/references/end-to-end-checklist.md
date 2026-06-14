# AWS End-to-End Security Checklist

> **Provenance:** CIS AWS Foundations v3.0 + AWS Well-Architected Security Pillar — reviewed 2026-06-14.  
> Source registry: [registry/provenance.yaml](../../../registry/provenance.yaml)

Use with `aws-security-best-practices` skill. Mark each item before sign-off.

## Governance
- [ ] AWS Organizations with OU structure (Security, Workloads, Sandbox)
- [ ] SCPs on all OUs (region lock, no root, deny public S3 where required)
- [ ] Delegated admin for GuardDuty, Security Hub, Macie
- [ ] Control Tower or account factory baseline
- [ ] Mandatory tags: Owner, Environment, DataClassification

## IAM & SSO
- [ ] IAM Identity Center — no IAM users for humans (except break-glass)
- [ ] MFA enforced for all human access
- [ ] No access keys on IAM users or roles used by apps
- [ ] Permission boundaries on creatable roles
- [ ] IAM Access Analyzer enabled; external access remediated
- [ ] EKS IRSA configured for agents (OIDC, scoped trust policy)

## KMS & Secrets
- [ ] CMK per environment; automatic rotation enabled
- [ ] Secrets Manager for app secrets; rotation scheduled
- [ ] S3 SSE-KMS on sensitive buckets
- [ ] RDS/EBS encrypted with CMK
- [ ] CloudTrail log file validation + KMS encryption

## Network
- [ ] VPC segmentation; no public IPs on databases
- [ ] Security groups default deny inbound
- [ ] VPC Flow Logs to central store
- [ ] VPC endpoints for S3, KMS, Secrets Manager, STS
- [ ] AWS WAF on public ALB/CloudFront
- [ ] Network Firewall or equivalent egress control (if required)

## Compute & EKS
- [ ] EC2 IMDSv2 required
- [ ] EKS private endpoint or restricted public
- [ ] Pod security standards / PSA enforced
- [ ] Container image scan (ECR)

## Data
- [ ] S3 Block Public Access account-wide
- [ ] S3 versioning + MFA delete on audit buckets
- [ ] RDS not publicly accessible; SSL enforced

## Logging & Detection
- [ ] Organization CloudTrail to log archive account
- [ ] AWS Config enabled with conformance packs
- [ ] GuardDuty org-wide
- [ ] Security Hub standards enabled (CIS, FSBP)
- [ ] Alerts on root login, IAM policy change, KMS delete

## Compliance & Ops
- [ ] CIS AWS Benchmark gaps tracked
- [ ] Incident response runbook linked to GuardDuty findings
- [ ] Backup encrypted; restore tested quarterly

## Agent / MCP
- [ ] Agent uses IRSA/instance profile only
- [ ] MCP via Bastion proxy
- [ ] AIV design rules pass on agent code PRs
