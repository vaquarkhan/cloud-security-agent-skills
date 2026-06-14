---
name: multi-cloud-security-posture
description: End-to-end cross-cloud security baseline — unified identity, encryption, network, logging, SIEM, compliance mapping, hybrid patterns, and control ownership when environment is unknown or multi-cloud.
---

# Multi-Cloud Security Posture (End-to-End)

## Overview

Use when the environment is **unknown**, **hybrid**, or **multi-account/multi-cloud**. Establishes a **unified baseline** then routes to per-cloud skills for depth. Nothing omitted at the control-framework level.

---

## 1. Unified control framework

Every in-scope cloud must implement **all** rows below. Map to cloud-native services in section 2.

| Domain | Requirement | Success criteria |
|--------|-------------|------------------|
| **Governance** | Org/account structure, tagging, policy guardrails | SCPs/policies deny public data, unencrypted storage |
| **Identity** | SSO, MFA, no static workload keys | 100% human access via IdP; agents use platform identity |
| **Encryption (at rest)** | CMK/HSM for data stores | No unencrypted prod databases or object storage |
| **Encryption (in transit)** | TLS 1.2+ everywhere | No plain HTTP on public endpoints |
| **Network** | Segmentation, default deny, private data plane | No DB with public IP; flow logs enabled |
| **Secrets** | Central vault per cloud | Zero secrets in git/CI/images |
| **Logging** | Immutable audit trail | Org-wide trail to log archive account |
| **Detection** | CSPM + threat detection | Critical findings SLA < 24h |
| **Vulnerability** | VM + container scanning | Critical CVE patch SLA defined |
| **Backup/DR** | Encrypted backups, tested restore | Quarterly restore test |
| **MCP/agent** | Bastion gateway, AIV gate | No direct MCP; PR design rules pass |
| **Compliance** | Map to CIS + regulatory framework | Evidence collection automated where possible |

---

## 2. Cloud service mapping

### Identity & access

| Control | AWS | Azure | GCP | OCI | IBM | Alibaba | PCF |
|---------|-----|-------|-----|-----|-----|---------|-----|
| Human SSO | IAM Identity Center | Entra ID | Cloud Identity / IdP | IDCS / federated | IBMid | RAM federated | UAA SAML |
| Workload ID | IAM role / IRSA | Managed identity | Workload Identity | Resource principal | Trusted Profile | ECS RAM / RRSA | UAA client / K8s SA |
| Key vault | Secrets Manager | Key Vault | Secret Manager | OCI Vault | Secrets Manager | Secrets Manager | CredHub |
| Crypto keys | KMS | Key Vault keys | Cloud KMS | Vault keys | Key Protect/HPCS | KMS | CredHub + cloud KMS |
| Policy guardrails | SCP | Azure Policy | Org constraints | IAM + Security Zones | Account policies | Control policy | ASG / Isolation Segment |

### Network & edge

| Control | AWS | Azure | GCP | OCI | IBM | Alibaba | PCF |
|---------|-----|-------|-----|-----|-----|---------|-----|
| Segmentation | VPC + SG | VNet + NSG | VPC + firewall | VCN + NSG | VPC SG | VPC + SG | ASG / Network Policy |
| WAF | AWS WAF | App Gateway WAF | Cloud Armor | OCI WAF | CIS | Cloud WAF | Route service |
| Private link | VPC endpoints | Private Link | Private Service Connect | Private Endpoint | Private Path | PrivateLink | Internal routes |
| Flow logs | VPC Flow Logs | NSG flow logs | VPC Flow Logs | VCN Flow Logs | Flow logs | VPC Flow Logs | Platform logs |

### Logging & detection

| Control | AWS | Azure | GCP | OCI | IBM | Alibaba | PCF |
|---------|-----|-------|-----|-----|-----|---------|-----|
| Audit API | CloudTrail | Activity Log | Audit Logs | Audit service | Activity Tracker | ActionTrail | CF audit events |
| SIEM | Security Lake / Splunk | Sentinel | Chronicle / SCC | Logging Analytics | QRadar/SIEM | SLS | Loggregator → SIEM |
| CSPM | Security Hub | Defender CSPM | SCC | Cloud Guard | SCC | Security Center | Underlying IaaS |
| Threat | GuardDuty | Defender | SCC findings | Cloud Guard | — | Security Center | — |

---

## 3. Session routing (agent workflow)

```
1. Introspect runtime cloud(s)
2. Load zero-trust-identity-and-secrets
3. If single cloud → load ONE primary cloud skill (full depth)
4. If hybrid → this skill + EACH in-scope cloud skill
5. Load mcp-bastion-security-gateway
6. Assess → harden → mcp-test validate → AIV gate
```

### Primary cloud skills

| Cloud | Skill |
|-------|-------|
| AWS | `aws-security-best-practices` |
| Azure | `azure-security-best-practices` |
| GCP | `gcp-security-best-practices` |
| OCI | `oci-oracle-cloud-security` |
| IBM | `ibm-cloud-security-best-practices` |
| Alibaba | `alibaba-cloud-security-best-practices` |
| PCF/Tanzu | `vmware-tanzu-pcf-security` |

Each cloud skill includes IAM, KMS/vault, network, compute, data, logging, compliance, checklists, and red flags.

---

## 4. Hybrid and multi-cloud patterns

### Identity federation

- **Single corporate IdP** → all cloud SSO
- **No duplicate local users** per cloud
- **Consistent group naming** mapped to cloud RBAC

### Tagging standard (all clouds)

| Tag | Values | Use |
|-----|--------|-----|
| `Environment` | prod, staging, dev, sandbox | Policy scope |
| `DataClassification` | public, internal, confidential, restricted | Encryption, access |
| `Owner` | team email / cost center | Accountability |
| `Application` | app id | Resource grouping |

### Central SIEM

Normalize to common schema (OCSF where possible):

- AWS CloudTrail → S3 → SIEM
- Azure Activity Log → Log Analytics / Sentinel
- GCP Audit Logs → BigQuery / Chronicle
- OCI Audit → Object Storage → SIEM
- IBM Activity Tracker → COS
- Alibaba ActionTrail → SLS
- PCF audit events → Loggregator nozzle

### Data residency

- Document **home region** per data class per cloud
- **Cross-border transfer** assessment (GDPR, etc.)
- **Replication** only to approved regions

---

## 5. Agent stack (this repo)

```
IdentityManager → Cloud skill(s) → Bastion → MCP server → mcp-test → AIV
```

Tools: `echo_security_context`, `assess_cloud_posture`, `validate_security_controls`

---

## 6. Assessment methodology

### Phase 1 — Discover
- Accounts, subscriptions, projects, tenancies
- Data classification inventory
- Agent/MCP deployment locations

### Phase 2 — Baseline
- Score each unified control (section 1) 0–3
- Pull CSPM posture (Security Hub, SCC, etc.)

### Phase 3 — Gap remediate
- Priority: public data → static keys → missing audit → network exposure
- Per-cloud skill checklists

### Phase 4 — Validate
- `mcp-test` security suite
- AIV design rules
- Manual pen test scope for critical apps

### Phase 5 — Operate
- Continuous compliance rules
- Monthly finding review
- Quarterly access review

---

## 7. Compliance mapping (high level)

| Framework | Cross-cloud focus |
|-----------|-------------------|
| CIS Benchmark | Per-cloud benchmark skill sections |
| SOC 2 | Logging, access control, encryption, change management |
| PCI DSS | Network segmentation, key management, no static keys |
| HIPAA | Encryption, audit, minimum necessary access |
| ISO 27001 | ISMS aligned to sections 1–6 above |
| NIST CSF | Identify, Protect, Detect, Respond, Recover mapped to controls |

Detailed control IDs live in each cloud skill compliance section.

---

## 8. Verification checklist

- [ ] Every in-scope cloud has named primary skill loaded
- [ ] All 12 unified controls (section 1) scored
- [ ] No cloud excluded from org-wide audit logging
- [ ] Tagging standard applied ≥ 95% resources
- [ ] SIEM ingestion verified for each audit source
- [ ] Bastion + AIV enabled in CI
- [ ] Static key scan clean (AIV + manual)
- [ ] Hybrid identity federation documented

---

## 9. Red flags

- "We use AWS for prod and Azure for dev" with no logging in dev
- Security review scoped to one cloud but data spans three
- Different secret policies per cloud with no central vault strategy
- MCP agents in multiple clouds without Bastion on each path

---

## Related skills

- `cloud-well-architected-frameworks` — AWS/Azure/GCP/OCI/IBM/Alibaba/PCF WAF pillars
- `using-cloud-security-agent-skills` — session start
- `zero-trust-identity-and-secrets`
- All seven cloud skills
- `mcp-bastion-security-gateway`, `mcp-security-testing-harness`, `pr-integrity-aiv-gate`
