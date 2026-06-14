---
name: aws-security-best-practices
description: End-to-end AWS security — Organizations, IAM, SSO, SCPs, KMS, Secrets Manager, VPC, WAF, GuardDuty, Security Hub, CloudTrail, Config, EKS IRSA, S3/RDS/EBS encryption, compliance (CIS, PCI, HIPAA), and zero static keys for agents.
---

# AWS Security Best Practices (End-to-End)

## Overview

Use this skill for **any** AWS security assessment, hardening, audit prep, or agent deployment review. Covers identity through incident response. Pair with `zero-trust-identity-and-secrets` and `mcp-bastion-security-gateway`.

**In-repo identity:** `AWSCredentialChainManager` — IAM roles, IRSA, instance profiles only. **Never** embed `AKIA*` access keys.

---

## 1. Organization and account governance

### AWS Organizations

- Enable **Organizations** with consolidated billing; use **OU structure**: Security, Infrastructure, Workloads (prod/nonprod), Sandbox, Suspended
- **Service Control Policies (SCPs)** on every OU — deny list at root, allow granular at workload OUs
- **Block public AMIs/sharing** where not required; restrict `us-east-1` / opt-in regions if data residency applies
- **Delegated administrator** accounts for GuardDuty, Security Hub, Macie, Firewall Manager — not the management account for daily workloads

### Recommended SCP deny patterns

| SCP intent | Example constraint |
|------------|-------------------|
| No root usage | Deny all actions when `aws:PrincipalArn` is root |
| Region lock | Deny all except approved regions (`aws:RequestedRegion`) |
| No IAM users with keys | Deny `iam:CreateAccessKey` except break-glass role |
| Encryption required | Deny S3 `PutObject` without SSE-KMS on sensitive buckets |
| Leave org protection | Deny `organizations:LeaveOrganization` |

### Account factory

- **Control Tower** or custom **Account Factory** for baseline: CloudTrail, Config, GuardDuty, default VPC removal optional
- **Alternate contacts** (security, billing, operations) set on every account
- **Account alias** and tagging standard: `Owner`, `Environment`, `DataClassification`, `CostCenter`

---

## 2. Identity and access management (IAM)

### Humans

- **IAM Identity Center (SSO)** — sole human access path; no long-lived IAM user console passwords
- **MFA enforced** for all human principals (hardware FIDO2 preferred for admins)
- **Permission sets** time-bound where possible; separate admin / read-only / developer sets
- **Break-glass** root: MFA on root, no access keys, usage monitored via CloudTrail + alert

### Workloads and agents

- **IAM roles** only — EC2 instance profiles, ECS task roles, Lambda execution roles, **EKS IRSA** for agents
- **No access keys** in CI, containers, or agent code; use OIDC federation (GitHub Actions, GitLab) with `AssumeRoleWithWebIdentity`
- **Permission boundaries** on all roles that humans can create; prevents privilege escalation
- **Session policies** for temporary elevation; max session duration 1h for sensitive roles

### IAM policy design

- **Least privilege** — one role per workload function; avoid `*` on `*` except SCP-guarded automation roles
- **Condition keys**: `aws:SourceVpc`, `aws:SourceIp`, `aws:PrincipalTag`, `aws:SecureTransport`, `aws:MultiFactorAuthPresent`
- **Resource-level** permissions on S3 ARNs, KMS keys, secrets — not `Resource: *` for data planes
- **IAM Access Analyzer** — external access findings remediated; unused access reviewed quarterly
- **Access Analyzer for IAM** — validate policies before deploy (CI gate)

### IAM anti-patterns (reject in review)

- IAM users with active access keys for applications
- `AdministratorAccess` on workload roles
- Wildcard `s3:*` on `Resource: *`
- Trust policies with `"AWS": "*"` or overly broad external accounts
- Cross-account roles without external ID + least privilege

### EKS / agent IRSA checklist

- [ ] OIDC provider registered for cluster
- [ ] Service account annotated with role ARN
- [ ] Role trust policy scoped to `system:serviceaccount:namespace:sa-name`
- [ ] Role policy grants only APIs needed (e.g., `secretsmanager:GetSecretValue` on one secret ARN)

---

## 3. Encryption and key management (KMS)

### KMS fundamentals

- **Customer managed keys (CMK)** for regulated data; AWS managed keys acceptable only for non-sensitive tiers
- **Key policies** + IAM — dual authorization; deny `kms:DisableKey`, `kms:ScheduleKeyDeletion` except security admin
- **Automatic key rotation** enabled on CMKs (annual material rotation)
- **Multi-Region keys (MRK)** only when DR/active-active truly required — understand tradeoffs
- **Grant restrictions** — avoid grants unless legacy integration requires; prefer IAM policies

### Service encryption matrix

| Service | At rest | In transit | Notes |
|---------|---------|------------|-------|
| S3 | SSE-KMS (CMK) | TLS 1.2+ (`aws:SecureTransport`) | Bucket policy deny unencrypted |
| EBS | Encrypt by default (account setting) | N/A | Launch template enforcement |
| RDS / Aurora | KMS CMK | TLS in connection string | IAM DB auth where supported |
| DynamoDB | AWS owned or CMK | HTTPS API only | Point-in-time recovery for prod |
| EFS | KMS | TLS for mount targets | |
| Secrets Manager | KMS CMK | TLS | Rotation Lambda/custom |
| SSM Parameter Store | SecureString + KMS | TLS | Never `String` for secrets |
| EKS secrets (etcd) | KMS envelope encryption | TLS to API | Enable `encryptionConfig` |
| CloudTrail logs | SSE-KMS on S3 bucket | TLS | Log file validation ON |
| SNS/SQS | KMS CMK for sensitive | TLS | Queue policy least privilege |

### TLS and certificates

- **ACM** for public TLS on ALB/CloudFront/API Gateway
- **TLS 1.2 minimum** on all load balancers; disable legacy ciphers
- **Certificate transparency** monitoring for domain hijack detection

---

## 4. Network security

### VPC design

- **Multi-AZ** private subnets for apps and data; **public subnets** only for NAT/ALB ingress
- **No public IPs** on databases, internal agents, or batch workers
- **VPC Flow Logs** to S3 (Parquet) + Athena or to CloudWatch — retention per compliance
- **Network ACLs** — subnet-level deny for known bad CIDRs; SGs primary control
- **Security groups** — default deny ingress; document every rule; no `0.0.0.0/0` on admin ports (22, 3389)

### Connectivity

- **VPC endpoints (Interface/Gateway)** for S3, DynamoDB, STS, KMS, Secrets Manager, ECR, CloudWatch Logs — keep traffic off internet
- **PrivateLink** for SaaS and cross-account service consumption
- **Transit Gateway** hub-spoke; **Network Firewall** or third-party NGFW on egress path
- **AWS WAF** on CloudFront, ALB, API Gateway — OWASP Core Rule Set + rate limiting
- **Shield Advanced** for DDoS-critical public surfaces

### DNS and edge

- **Route 53** DNSSEC where applicable
- **CloudFront** signed URLs/cookies for sensitive static content

---

## 5. Compute and containers

### EC2

- **IMDSv2 required** (`HttpTokens: required`) — block IMDSv1 credential theft
- **SSM Session Manager** instead of SSH; no bastion SSH keys in prod
- **Approved AMIs** via EC2 Image Builder; scan with Inspector
- **Patching** via SSM Patch Manager; critical CVE SLA defined

### ECS / Fargate

- Task roles (not instance role) for app permissions
- **No privileged containers** unless documented exception
- Read-only root filesystem where possible; seccomp/AppArmor patterns
- ECR image scanning on push; block critical vulnerabilities in deploy pipeline

### EKS

- **Private API endpoint** or restricted public CIDR
- **Pod Security Standards** (restricted baseline minimum)
- **Network policies** (Calico/Cilium) default deny east-west
- **Secrets Store CSI driver** + IRSA for secret mounts
- **Control plane logging** — api, audit, authenticator, scheduler, controllerManager

### Lambda

- Least-privilege execution role per function
- **VPC** only when needed (cold start vs isolation tradeoff)
- Environment variables encrypted with KMS; secrets from Secrets Manager
- **Function URLs** disabled unless authenticated

---

## 6. Storage and data

### S3

- **Block Public Access** — account and bucket level, enforced by SCP
- Bucket policies: deny `s3:PutObject` without encryption; deny insecure transport
- **Versioning** + **MFA Delete** on critical buckets
- **Object Lock** (WORM) for compliance retention where required
- **Macie** for sensitive data discovery (PII, credentials in objects)
- **Access logging** to separate audit bucket; log bucket no public access

### RDS / Aurora / DocumentDB / Redshift

- Not publicly accessible
- Encryption at rest with CMK; snapshots encrypted
- **Automated backups** + cross-region copy for DR
- **Enhanced monitoring** and Performance Insights where needed
- Redshift: column-level encryption, concurrency scaling limits

### DynamoDB

- CMK for regulated tables; PITR enabled
- **IAM fine-grained access control** where applicable
- Streams encrypted; consumer roles least privilege

---

## 7. Application integration and APIs

- **API Gateway** — IAM auth, Cognito, or mTLS for internal APIs; WAF attached
- **ALB** — access logs to S3; drop invalid headers
- **SQS/SNS/EventBridge** — resource policies deny cross-account unless explicit
- **Step Functions** — logging level ALL for sensitive workflows

---

## 8. Secrets and credentials

- **Secrets Manager** preferred for rotation (RDS, Redshift, custom Lambda rotation)
- **SSM Parameter Store** SecureString tier for config secrets
- **No secrets in Lambda env** plain text, user-data scripts, or CloudFormation parameters without `NoEcho`
- **Git secrets scanning** + AIV gate in this repo — block `AKIA`, `ASIA` patterns

---

## 9. Logging, monitoring, and detection

### Mandatory logging

| Log type | Destination | Retention |
|----------|-------------|-----------|
| CloudTrail management | S3 + KMS, org trail | 1–7 years per policy |
| CloudTrail data events | S3 sensitive buckets, Lambda | Per data class |
| VPC Flow Logs | S3 Parquet / CloudWatch | 90d–1y |
| ALB/WAF/CloudFront access | S3 | Per compliance |
| EKS control plane | CloudWatch Logs | 90d+ |
| Route 53 query logs | CloudWatch | As needed |

- **CloudTrail log file validation** enabled
- **CloudWatch alarms** on root login, IAM policy changes, KMS disable, S3 public access changes
- **GuardDuty** org-wide with delegated admin; S3 Protection, EKS Audit Log Monitoring, Malware Protection as needed
- **Security Hub** — CIS AWS Foundations Benchmark, PCI DSS, NIST 800-53 standards
- **AWS Config** — record all resources; conformance packs for CIS; remediate via SSM Automation
- **Inspector** — EC2, ECR, Lambda vulnerability scanning

### SIEM integration

- CloudTrail → EventBridge → SQS → on-prem SIEM or **OpenSearch** / **Security Lake**
- Normalize with OCSF where possible; correlate GuardDuty findings

---

## 10. Backup, DR, and resilience

- **AWS Backup** plans with vault encryption (CMK), cross-region copy for tier-1
- **RTO/RPO** documented per workload; test restore quarterly
- **DynamoDB global tables / RDS cross-region read replicas** per DR strategy

---

## 11. Compliance mappings (high level)

| Framework | AWS anchor services |
|-----------|---------------------|
| CIS AWS Foundations | Config, Security Hub, IAM, CloudTrail |
| PCI DSS | KMS, WAF, segmentation, logging, IAM |
| HIPAA | BAA services only, encryption, audit controls |
| SOC 2 | CloudTrail, Config, access reviews, change management |
| FedRAMP | GovCloud partition, authorized services list |

Document **shared responsibility** — AWS vs customer controls in assessment reports.

---

## 12. Agent and MCP deployment on AWS

- Agent pods on EKS with **IRSA**; no `AWS_ACCESS_KEY_ID` in manifests
- MCP server behind **Bastion** (`bastion.yaml`); traffic via `agent.bastion_proxy`
- **VPC endpoints** so agent never needs NAT for AWS API calls where possible
- **Presidio PII** redaction before LLM context (Bastion pillar)
- **CloudWatch** metrics on agent tool call rates; align with Bastion `rate_limit`

---

## 13. End-to-end verification checklist

### Identity
- [ ] No IAM user access keys for workloads
- [ ] SSO + MFA for humans
- [ ] SCPs on all OUs
- [ ] Access Analyzer clean for external access

### Encryption
- [ ] EBS encryption by default
- [ ] S3 buckets deny unencrypted objects
- [ ] RDS/DynamoDB use CMK where required
- [ ] KMS key policies least privilege

### Network
- [ ] No public RDS/Redis/OpenSearch
- [ ] Flow logs enabled
- [ ] WAF on public HTTP(S)

### Logging & detection
- [ ] Org CloudTrail all regions
- [ ] GuardDuty + Security Hub enabled
- [ ] Config recording with conformance pack

### Secrets
- [ ] Secrets Manager/SSM for all credentials
- [ ] Rotation configured

### Agent
- [ ] IRSA or instance role only
- [ ] Bastion MCP path enforced

---

## 14. Red flags (stop and remediate)

- Access keys in Git history or agent env
- S3 bucket `PublicAccessBlock` disabled
- Security group `0.0.0.0/0` on port 22 or 5432
- CloudTrail disabled or single-region only in prod org
- KMS key pending deletion
- Root account used for daily operations

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected:** see `cloud-well-architected-frameworks` — AWS WA Tool, six pillars, cross-cloud matrix.

## 15. Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `mcp-security-testing-harness`
- `multi-cloud-security-posture` (hybrid estates)
