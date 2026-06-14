---
name: alibaba-cloud-security-best-practices
description: End-to-end Alibaba Cloud security — RAM, STS, ECS instance RAM roles, KMS, Secrets Manager, VPC, Security Group, Cloud Firewall, WAF, ActionTrail, Security Center, and agent identity without AccessKey in code.
---

# Alibaba Cloud Security Best Practices (End-to-End)

## Overview

Complete Alibaba Cloud (Aliyun) security. Agents use **ECS instance RAM role** + STS (`EcsRamRoleCredentialProvider`) — **never** AccessKey ID/Secret in application code.

---

## 1. Account and resource organization

- **Resource Directory** (multi-account) — Log Archive, Security Audit, Workload accounts (Prod/NonProd)
- **Resource Group** per application/environment within account
- **Tagging** — `Environment`, `DataClassification`, `Owner`, `Project`
- **Control policies** (类似 SCP) on RD folders — deny public OSS, deny RAM user creation without MFA
- **Cloud Config** rules at org level for continuous compliance

---

## 2. Resource Access Management (RAM)

### Human access

- **Alibaba Cloud account** root — MFA, no daily use; break-glass only
- **RAM users** federated from corporate IdP (SAML/OIDC) where possible
- **MFA mandatory** for all RAM users with console access
- **RAM groups** by job function; policies on groups not individuals

### RAM roles and STS

- **RAM roles** for cross-account trust and service-to-service
- **ECS instance RAM role** — agent/workload identity (this repo pattern)
- **RRSA** (RAM Role for Service Account) for ACK (Kubernetes) pods
- **STS AssumeRole** with **external ID** for third-party access; session duration minimum needed

### Least privilege

- **System policies** avoided when custom policy can scope resource ARN
- **Resource-level authorization** on OSS buckets, RDS, KMS keys
- **Permission boundary** on RAM roles used by automation
- **AccessKey** for RAM users — disable creation via control policy; rotate 90d if legacy

### Agent identity

```python
# Pattern in this repo — EcsRamRoleCredentialProvider
# Platform sets role name; no keys in env or code
```

---

## 3. KMS and Secrets Manager

### Key Management Service (KMS)

- **Customer master keys (CMK)** per environment; **HSM** type for regulated data
- **Automatic key rotation** annual for symmetric CMKs
- **RAM policies** on `kms:Encrypt`, `kms:Decrypt` scoped to key ARN
- **Envelope encryption** for OSS, RDS, ECS disks, Log Service

### Secrets Manager

- **Secrets** for DB passwords, third-party API keys
- **Rotation** via Function Compute where supported
- **Audit** via ActionTrail on `GetSecretValue`

### Encryption matrix

| Service | At rest | In transit |
|---------|---------|------------|
| OSS | SSE-KMS with CMK | HTTPS only; reject HTTP |
| RDS | TDE with KMS | SSL required |
| ECS disks | Encrypted system/data | N/A |
| NAS | KMS encryption | NFS over VPC |
| Table Store / MongoDB | KMS | TLS |

---

## 4. Network security (VPC)

### VPC architecture

- **VPC per environment** or shared VPC with subnet isolation
- **Public subnet** — SLB, NAT only; **private subnet** — ECS, RDS, ACK nodes
- **No public IP** on databases or internal agents
- **VPC Flow Logs** — enable and ship to Log Service / SIEM

### Security groups vs NACLs

- **Security groups** — stateful, attach to ECS ENI; default deny inbound
- **Network ACLs** — subnet-level deny rules for known bad CIDRs
- **Least privilege** — app tier only from SLB SG; DB only from app SG

### Connectivity

- **PrivateLink** / **VPC endpoints** for OSS, KMS, Log Service without public internet
- **Cloud Enterprise Network (CEN)** for multi-VPC and hybrid
- **VPN Gateway / Express Connect** — encrypted hybrid links

### Edge protection

- **Cloud Firewall** — centralized egress/ingress control, IPS
- **WAF** on SLB/API Gateway — OWASP, CC protection, bot defense
- **Anti-DDoS** Pro on critical public IPs

---

## 5. Compute and ACK (Kubernetes)

### ECS

- **Security hardening** — CIS Alibaba Cloud Linux benchmark
- **No SSH password**; key pairs or **Bastionhost** for access
- **Cloud Assistant** for patch management
- **Anti-virus / Security Center** agent on all instances

### ACK (Container Service for Kubernetes)

- **Private cluster** API endpoint
- **RRSA** for pod-level RAM roles (preferred over node-wide role)
- **Network policies** default deny
- **Image scan** in Container Registry (ACR)
- **Secrets** from KMS Secrets Manager / External Secrets — not plain K8s secrets in git

---

## 6. Data protection

### Object Storage Service (OSS)

- **Block public access** at bucket and account level
- **RAM policy** deny `oss:PutBucketAcl` public
- **Versioning** + **WORM** (compliance retention) for audit buckets
- **Cross-region replication** encrypted with same CMK policy

### RDS / PolarDB

- **Private network** only; whitelist minimal SG CIDRs
- **SSL** enforced; **TDE** with KMS
- **Audit log** to Log Service; **SQL audit** for sensitive DBs

---

## 7. Logging, audit, and threat detection

| Service | Purpose |
|---------|---------|
| ActionTrail | All API management and data events |
| Log Service (SLS) | Central log store and analysis |
| Security Center | Baseline, vuln scan, anomaly, compliance check |
| Cloud Config | Resource compliance rules |
| SIEM integration | Export trails to Splunk/Datadog/on-prem |

- **ActionTrail** — organization trail to Log Archive account OSS (immutable)
- **Alerts** on: `CreateAccessKey`, `AttachPolicy`, `PutBucketPolicy` public, `DeleteTrail`
- **Security Center** — enable all modules; auto-fix where safe with approval

---

## 8. Compliance

- **Alibaba Cloud compliance certifications** (ISO, SOC, MLPS 等) — map shared responsibility
- **CIS Alibaba Cloud Benchmark** via Security Center + manual evidence
- **MLPS** (China) — data localization and logging requirements if applicable

---

## 9. Agent / MCP on Alibaba Cloud

- ECS or ACK with **instance RAM role / RRSA**
- `ALIBABA_CLOUD_ECS_METADATA` — role from metadata service
- Secrets from Secrets Manager at runtime
- MCP via **Bastion gateway** only; ActionTrail logs all cloud API from agent role

---

## 10. Verification checklist

- [ ] Resource Directory with control policies
- [ ] No AccessKey on agent workloads
- [ ] ECS RAM role or RRSA configured
- [ ] KMS CMK for prod OSS/RDS/disks
- [ ] OSS public access blocked
- [ ] ActionTrail org-wide to Log Archive
- [ ] Security Center all features on
- [ ] Cloud Firewall + WAF on public entry points
- [ ] VPC Flow Logs enabled

---

## 11. Red flags

- AccessKey ID/Secret in code, env, or CI variables
- OSS bucket ACL public-read
- RDS `0.0.0.0/0` on whitelist
- RAM policy `Action: "*"` on `Resource: "*"` for service role
- ActionTrail disabled or single-region only without org trail

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected:** see `cloud-well-architected-frameworks` — Alibaba Cloud WAF, six pillars.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
