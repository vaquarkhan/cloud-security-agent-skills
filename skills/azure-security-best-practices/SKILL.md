---
name: azure-security-best-practices
description: End-to-end Azure security — Entra ID, Conditional Access, PIM, RBAC, Managed Identity, Key Vault, Defender for Cloud, Purview, Private Link, NSGs, Azure Firewall, WAF, Monitor, Sentinel, Policy, encryption, and zero client secrets.
---

# Azure Security Best Practices (End-to-End)

## Overview

Complete Azure security reference for assessments, landing zones, and agent workloads. Use with `AzureDefaultCredentialManager` — **no client secrets in code**.

---

## 1. Tenant and management group governance

- **Management groups** hierarchy: Root → Platform → Landing zones (corp/online) → Subscriptions
- **Azure Policy** at MG level — deny public IP on NICs, require tags, enforce TLS, require Key Vault for secrets
- **Blueprint / Landing zone accelerator (ALZ)** for baseline: activity logs, Defender, DDoS, hub-spoke network
- **Subscription vending** via DevOps pipeline; no manual subscription sprawl
- **Activity log** export to locked Storage + Log Analytics — retention per compliance

---

## 2. Identity — Microsoft Entra ID

### Human identity

- **Conditional Access**: MFA all users; block legacy auth; require compliant/hybrid Azure AD joined device for admin
- **Privileged Identity Management (PIM)** — just-in-time for Owner, UAA admin, Key Vault Officer; activation requires MFA + approval
- **Entra ID Protection** — risk-based policies (sign-in risk, user risk)
- **Break-glass accounts** — cloud-only, excluded from CA with monitoring alerts (use sparingly)
- **Guest access** — B2B with restricted permissions; periodic access reviews

### Workload identity

- **System-assigned and user-assigned Managed Identity** for all Azure-hosted agents — **no service principal secrets**
- **Workload identity federation** — GitHub Actions, Kubernetes OIDC to Entra app without secrets
- **Federated credentials** on app registrations for CI/CD and AKS workload identity

### RBAC

- **Least privilege** at resource group / resource scope — avoid Subscription Owner for apps
- **Custom roles** when built-in too broad; document actions not in role
- **Deny assignments** for critical resources (production Key Vault, Terraform state)
- **Access reviews** quarterly for privileged roles

### Anti-patterns

- Service principal with client secret in pipeline variable (plain text)
- `Contributor` on subscription for application MI
- Local AD sync accounts with weak password policy without CA

---

## 3. Key Vault and encryption

### Key Vault

- **RBAC authorization model** (preferred over access policies for new vaults)
- **Soft delete + purge protection** enabled
- **Private endpoint** — no public network access on prod vaults
- **HSM-backed keys** (Premium SKU) for regulated workloads
- **Key rotation** policy documented; automation via Key Vault rotation API / Functions
- Separate vaults per environment (dev/test/prod) and per data classification

### Encryption at rest

| Service | Control |
|---------|---------|
| Storage Account | CMK in Key Vault; infrastructure encryption optional |
| Azure SQL / MI | TDE with CMK; Always Encrypted for column-level |
| Cosmos DB | CMK; private endpoint |
| AKS etcd | Azure-managed or CMK via Disk Encryption Set |
| Managed Disks | DES with CMK |
| Blob | SSE with CMK; immutability policies for WORM |

### Encryption in transit

- **TLS 1.2+** minimum on App Service, Application Gateway, Front Door
- **HTTPS only** on Storage; secure transfer required

---

## 4. Network security

### Hub-spoke topology

- **Azure Firewall** or NVA in hub; forced tunneling to on-prem or secure egress
- **DDoS Network Protection** on prod VNets with public IPs
- **NSGs** — default deny inbound; application security groups (ASGs) for tier segmentation
- **UDRs** — route all egress through firewall; no direct internet from spoke without inspection

### Private connectivity

- **Private Link** for Storage, Key Vault, SQL, Cosmos, ACR, Monitor, Synapse
- **Private DNS zones** linked to hub/spoke VNets
- **Service endpoints** legacy — prefer Private Link for new designs

### Application edge

- **Application Gateway WAF** or **Front Door WAF** — OWASP 3.2, bot protection, rate limits
- **Internal load balancers** for backend tiers; no public PIPs on app servers

### DNS

- **Azure DNS Private Resolver** for hybrid; log DNS queries for sensitive zones

---

## 5. Compute and containers

### Virtual machines

- **Azure Bastion** instead of jump box SSH/RDP with public IP
- **Defender for Servers** Plan 2 — vulnerability assessment, EDR integration
- **Disk encryption** (ADE) or encrypted disks by default
- **Trusted Launch** / Secure Boot where supported
- **Automatic patching** via Update Management / Azure Automanage

### Azure Kubernetes Service (AKS)

- **Private cluster** API; authorized IP ranges if public API unavoidable
- **Azure CNI** with network policies (Calico/Azure NPM)
- **Workload identity** (OIDC + federated credential) — replace pod-managed identity legacy
- **Defender for Containers** — runtime threat detection
- **Azure Policy for AKS** — no privileged containers, required labels, allowed registries
- **Key Vault CSI provider** for secrets; no K8s secrets for credentials plain text

### App Service / Functions

- Managed identity for Key Vault references
- VNet integration + private endpoints for downstream
- Authentication enabled (Entra ID) on internal APIs

---

## 6. Data platform security

### Storage

- Disable public blob access account-wide
- **Immutable storage** for audit logs
- **Microsoft Defender for Storage** — malware scanning, suspicious access
- SAS tokens: user delegation SAS; shortest TTL; stored in Key Vault

### Databases

- **Azure SQL**: firewall deny public; private link; AAD-only admin where possible; auditing to Storage/LA
- **Synapse / Databricks**: workspace behind private link; CMK; Purview integration

### Purview and governance

- **Microsoft Purview** for data map, classification, lineage, access policies
- Sensitivity labels on SQL columns where applicable

---

## 7. Logging, monitoring, and SIEM

| Source | Destination |
|--------|-------------|
| Activity Log | Log Analytics + Archive Storage |
| Resource logs (Diagnostic settings) | LA / Event Hub / Storage |
| Entra sign-in / audit | Log Analytics |
| NSG flow logs | Traffic Analytics or Storage |
| Firewall logs | Log Analytics |
| Key Vault logs | Log Analytics — alert on secret get anomalies |

- **Microsoft Sentinel** — analytics rules, UEBA, SOAR playbooks
- **Defender for Cloud** Secure Score — track remediation; regulatory compliance dashboard
- **Alerts** to Action Groups → PagerDuty/Teams/email; no alert fatigue — tune thresholds

---

## 8. DevOps and supply chain

- **Azure DevOps / GitHub** OIDC to Entra — no long-lived SP secrets
- **ACR** — content trust, quarantine policy, Defender scan gate before deploy
- **Resource locks** on production RG (CanNotDelete)
- **Template specs** / Bicep with what-if and policy compliance scan in CI

---

## 9. Backup and DR

- **Azure Backup** with encryption; cross-region restore for tier-1
- **Site Recovery** for VM DR where RTO requires
- **Geo-redundant storage** for backup vault metadata

---

## 10. Compliance

- **Defender for Cloud** regulatory compliance (PCI, ISO 27001, SOC, HIPAA blueprint)
- **Azure Policy** initiatives mapped to CIS Microsoft Azure Foundations
- Document customer responsibilities in shared responsibility matrix

---

## 11. Agent / MCP on Azure

- Agent on AKS/App Service with **user-assigned MI**
- Key Vault secret refs for any human-configured material (not in git)
- **Private Link** to Azure OpenAI / other LLM endpoints if used
- Bastion MCP proxy mandatory; Presidio for PII in tool outputs

---

## 12. Verification checklist

### Identity
- [ ] CA: MFA + block legacy auth
- [ ] PIM for all privileged roles
- [ ] No SP secrets in repos/pipelines
- [ ] MI on all compute workloads

### Key Vault & encryption
- [ ] Purge protection ON
- [ ] Private endpoint on prod vaults
- [ ] CMK on storage/SQL as required

### Network
- [ ] No public DB endpoints
- [ ] Hub firewall inspecting egress
- [ ] WAF on public HTTP(S)

### Monitoring
- [ ] Activity + resource logs to LA
- [ ] Sentinel or SIEM integration
- [ ] Defender for Cloud enabled all subs

---

## 13. Red flags

- Client secret in ARM/Bicep/Terraform state unencrypted
- Storage account public blob access enabled
- SQL `0.0.0.0` firewall rule
- Global admin count > 5 without PIM
- Key Vault without soft delete

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected:** see `cloud-well-architected-frameworks` — Azure WAF, six pillars, cross-cloud matrix.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
