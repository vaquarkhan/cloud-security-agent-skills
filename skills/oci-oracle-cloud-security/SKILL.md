---
name: oci-oracle-cloud-security
description: End-to-end OCI security — IAM, compartments, dynamic groups, resource principals, OCI Vault/KMS, Cloud Guard, WAF, Security Zones, NSGs, VCN, logging, Data Safe, and agent identity via get_resource_principals_signer.
---

# Oracle Cloud Infrastructure (OCI) Security — End-to-End

## Overview

Complete OCI security for tenancies, workloads, and agents using **resource principals** (`OCIResourcePrincipalManager`). No API signing keys in application code.

---

## 1. Tenancy and compartment governance

- **Compartment hierarchy** mirrors org: Security, Network, SharedServices, Workloads (Prod/NonProd), Sandbox
- **Compartment quotas** and **budget alerts** on each major compartment
- **Tag defaults** — `Environment`, `DataClassification`, `Owner`, `CostCenter` applied at compartment create
- **Oracle Cloud Guard** enabled at root compartment with targets per compartment tree
- **Security Zones** on production compartments — max security recipe (see section 6)
- **IAM admin** limited to security compartment; no local users for daily ops — federate with IdP (SAML/OIDC)

---

## 2. Identity and access management (IAM)

### Human access

- **Identity Domains** (or federated IdP) with MFA for all users
- **Groups** map to job functions; **policies** attach to groups not individual users
- **No local passwords** for production admins where federation available
- **Break-glass** local admin: vaulted credentials, monitored login, quarterly test

### Policy language (least privilege)

```
Allow group DataEngineers to use buckets in compartment Workloads:Prod where target.bucket.name='logs-*'
Allow dynamic-group AgentPods to read secret-family in compartment Security where secret.name='agent-*'
```

- **Avoid** `manage all-resources in tenancy` except break-glass automation group with approval
- **Policy statements** version-controlled; CI validates syntax
- **Audit** via Audit service + IAM policy change alerts

### Dynamic groups and instance/resource principals

- **Dynamic groups** match rules on resource OCID, compartment, defined tags
- **Instance principal** for Compute/OKE node identity
- **Resource principal** for Functions, API Gateway, OKE pods (agent pattern)
- **Agent in this repo:** `get_resource_principals_signer()` + optional **OCI Vault** connectivity

### Service users / API keys

- **Eliminate API signing keys** for workloads — use dynamic groups + instance/resource principal
- If API keys exist for legacy: max 2 per user, rotate 90 days, store in Vault, never in git

---

## 3. OCI Vault and encryption

### Vault

- **Dedicated vaults** per environment; **HSM** protection level for regulated keys
- **Vault replication** across regions for DR keys
- **Secrets** versioned; rotation schedule for DB passwords/API tokens
- **Key usage** audit in Audit service; alert on `DeleteSecret`, `ScheduleKeyDeletion`

### Encryption by service

| Service | Encryption |
|---------|------------|
| Object Storage | SSE with Vault master key; bucket optional CMEK |
| Block Volumes | Vault key at create; encryption by default |
| Boot volumes | Same as block |
| Database (DBCS/ADB) | TDE transparent; Vault for wallet secrets |
| File Storage | Encryption at rest default |
| Streaming / Queue | Encrypt with Vault key |

### In transit

- **TLS 1.2+** on Load Balancer, API Gateway, Object Storage HTTPS
- **mTLS** on API Gateway for B2B where required

---

## 4. Network security (VCN)

### VCN design

- **Hub-spoke** or mesh with **DRG** (Dynamic Routing Gateway) for on-prem/cloud connectivity
- **Public subnets** only for load balancers and NAT; **private subnets** for apps and databases
- **No public IPs** on databases or internal agents
- **VCN Flow Logs** on all subnets — capture accepted/rejected; export to Logging Analytics / SIEM

### Security lists vs NSGs

- **NSGs (Network Security Groups)** preferred — stateful, attach to VNICs
- **Default deny** ingress; explicit allow per tier (LB → app → DB)
- **Security lists** backup layer — deny known bad CIDRs

### Connectivity

- **Service Gateway** for Oracle Services Network (Object Storage, etc.) without internet
- **NAT Gateway** for outbound internet from private subnets
- **Private Endpoint** for Object Storage, Database, etc.
- **FastConnect / IPsec VPN** — encrypt and monitor on-prem links

### Edge protection

- **OCI WAF** on Load Balancer — OWASP rules, rate limiting, bot management
- **DDoS protection** (always-on L3/L4; L7 options)

---

## 5. Compute and OKE (Kubernetes)

### Compute instances

- **Shielded instances** where available
- **Bastion service** for SSH — no public SSH on instances
- **OS Management** / custom patching SLAs
- **Custom images** hardened via CIS Oracle Linux benchmark

### OKE

- **Private API endpoint** or authorized CIDRs only
- **Pod security** — non-root, read-only root FS where possible
- **Network policies** (Calico) default deny
- **Workload identity** via **resource principal** for pods (agent pattern)
- **Secrets** from Vault CSI / OCI Secrets in Vault — not K8s secrets plain text
- **Image signing** and scan in OCIR (Artifact Registry)

---

## 6. Security Zones and Cloud Guard

### Security Zones

- Attach **Maximum Security Recipe** to prod compartment:
  - Deny public buckets
  - Deny public IP on databases
  - Require Vault encryption keys
  - Deny non-encrypted block volumes
- **Recipe violations** block resource creation — fix in IaC before deploy

### Cloud Guard

- **Targets** on root + workload compartments
- **Responders** — auto-remediate public bucket, open SG (with approval workflow)
- **Detector recipes**: Oracle-owned + custom for CIS
- Integrate findings with **Logging Analytics** and ticketing

---

## 7. Data protection

### Object Storage

- **No public buckets**; pre-authenticated requests (PAR) time-limited only
- **Retention rules** / immutable buckets for audit logs
- **Lifecycle** to Archive for cost with encryption maintained

### Database

- **Autonomous Database** — private endpoint, mTLS, Data Safe for SQL audit/user risk
- **Data Safe** — sensitive data discovery, user activity, security assessment
- **Database Vault** for separation of duties on DBCS where licensed

---

## 8. Logging and audit

| Service | Purpose |
|---------|---------|
| Audit service | All API calls — immutable export to Object Storage |
| Log Analytics | Central query across services |
| Service Connector Hub | Stream Audit/Logs to Object Storage, Functions, SIEM |
| VCN Flow Logs | Network forensics |
| WAF logs | Attack analysis |

- **Retention** aligned to compliance (often 1–7 years for audit in Object Storage with retention rules)
- **Alert rules** on Audit events: `CreatePolicy`, `DeleteVault`, `CreateApiKey`, `UpdateSecurityList`

---

## 9. Compliance

- **OCI compliance documents** (SOC, ISO, PCI) — map controls to shared responsibility
- **CIS Oracle Cloud Infrastructure Benchmark** via Cloud Guard + manual evidence
- **Data residency** — choose home region; understand cross-region replication implications

---

## 10. Agent / MCP on OCI

- Deploy on OKE/Functions with **resource principal**
- Set `OCI_RESOURCE_PRINCIPAL_VERSION`, `OCI_VAULT_ID` via platform — not in source
- Vault secrets for any human-provisioned config
- MCP **Bastion proxy** mandatory; audit tool calls via Logging + Bastion audit pillar

---

## 11. Verification checklist

- [ ] Cloud Guard enabled all targets
- [ ] Security Zone on prod compartment
- [ ] No API keys for workload identities
- [ ] Vault HSM for prod keys
- [ ] Audit log export to immutable bucket
- [ ] VCN Flow Logs on all subnets
- [ ] WAF on public LBs
- [ ] Data Safe enabled for Oracle DB estates
- [ ] Resource principal configured for agent

---

## 12. Red flags

- API signing key in source control
- Object Storage bucket public
- Database with public IP
- Policy `manage all-resources in tenancy` for app dynamic group
- Security Zone disabled on prod to "move faster"

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected:** see `cloud-well-architected-frameworks` — OCI Architecture Center, six pillars.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
