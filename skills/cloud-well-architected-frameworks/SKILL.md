---
name: cloud-well-architected-frameworks
description: One-stop shop for cloud Well-Architected Frameworks — AWS, Azure, GCP, OCI, IBM Cloud (Bluemix), Alibaba Cloud, VMware Tanzu PCF. All six pillars mapped cross-cloud with security depth, review tools, and links to per-cloud skills.
---

# Cloud Well-Architected Frameworks — One-Stop Shop

## Overview

Every major cloud publishes a **Well-Architected** (or equivalent) framework to evaluate workloads. This skill is the **single entry point** for all of them in this repo — same pillars, every provider, including **IBM Bluemix** (now IBM Cloud) and **Pivotal Cloud Foundry** (now **VMware Tanzu**).

**Use when:** architecture review, WAF workshop, migration assessment, RFP comparison, or “what does Azure call the AWS Security pillar?”

**Deep implementation:** load the matching cloud skill after this routing table.

| Cloud | Framework name | Deep skill in repo |
|-------|----------------|-------------------|
| AWS | AWS Well-Architected Framework | `aws-security-best-practices` |
| Azure | Microsoft Azure Well-Architected Framework | `azure-security-best-practices` |
| GCP | Google Cloud Architecture Framework | `gcp-security-best-practices` |
| OCI | Oracle Cloud Architecture Center / OCI Best Practices | `oci-oracle-cloud-security` |
| IBM / Bluemix | IBM Cloud Framework for Financial Services + IBM Garage / SCC | `ibm-cloud-security-best-practices` |
| Alibaba | Alibaba Cloud Well-Architected Framework | `alibaba-cloud-security-best-practices` |
| PCF / Tanzu | VMware Tanzu Reference Architecture + NIST CSF alignment | `vmware-tanzu-pcf-security` |

**Full pillar matrix:** [references/well-architected-pillar-matrix.md](references/well-architected-pillar-matrix.md)

---

## 1. Universal six pillars (cross-cloud vocabulary)

All providers align to these pillars (names vary slightly):

| # | Pillar | Question every review asks |
|---|--------|----------------------------|
| 1 | **Operational Excellence** | Can we run, observe, and improve the system safely? |
| 2 | **Security** | Is data and access protected at every layer? |
| 3 | **Reliability** | Does the system meet SLAs under failure and load? |
| 4 | **Performance Efficiency** | Right-sized resources with low latency? |
| 5 | **Cost Optimization** | Pay only for what delivers value? |
| 6 | **Sustainability** | Minimal carbon / energy for the workload? |

This repo is **security-first**; pillar 2 is expanded in every cloud skill. Other pillars are mapped here so nothing is missed in a WAF review.

---

## 2. AWS Well-Architected Framework

**Docs:** [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

| Pillar | AWS focus | Key services |
|--------|-----------|--------------|
| Operational Excellence | Runbooks, IaC, observability | CloudWatch, X-Ray, Systems Manager, OpsWorks |
| **Security** | IAM, detective controls, data protection | IAM, KMS, Secrets Manager, GuardDuty, Security Hub, WAF, Shield |
| Reliability | Multi-AZ, failover, quotas | Auto Scaling, Route 53, Backup, Elastic Disaster Recovery |
| Performance Efficiency | Right-sizing, caching, serverless | Compute Optimizer, ElastiCache, CloudFront, Lambda |
| Cost Optimization | Reserved, Savings Plans, tagging | Cost Explorer, Budgets, CUR, Trusted Advisor |
| Sustainability | Graviton, region selection, idle resources | Customer Carbon Footprint Tool, Graviton instances |

**Review tool:** AWS Well-Architected Tool (WA Tool) — workloads, lenses (Serverless, SaaS, **Security**, PCI, HIPAA, etc.)

**Security lens highlights:** strong identity foundation, traceability, secure application tiers, data classification, protecting network and compute.

→ Full IAM/KMS/network/logging: **`aws-security-best-practices`**

---

## 3. Microsoft Azure Well-Architected Framework

**Docs:** [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)

| Pillar | Azure focus | Key services |
|--------|-------------|--------------|
| Operational Excellence | DevOps, monitoring, safe deploy | Azure Monitor, App Insights, DevOps, Automation |
| **Security** | Identity, data protection, posture | Entra ID, Key Vault, Defender for Cloud, Purview, Sentinel |
| Reliability | HA, DR, self-healing | Availability Zones, Site Recovery, Traffic Manager, Azure Backup |
| Performance Efficiency | Scaling, CDN, caching | Azure Advisor, Front Door, Redis Cache, autoscale |
| Cost Optimization | Reservations, hybrid benefit | Cost Management, Advisor, Azure Hybrid Benefit |
| Sustainability | Carbon-aware design | Azure emissions dashboard, region selection |

**Review tool:** Azure Well-Architected Review (self-assessment) + **Defender for Cloud** regulatory compliance dashboard

**Design principles:** secure by design, identity as primary perimeter, encryption everywhere, minimize blast radius.

→ Full Entra ID/Key Vault/Defender: **`azure-security-best-practices`**

---

## 4. Google Cloud Architecture Framework

**Docs:** [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

| Pillar | GCP focus | Key services |
|--------|-----------|--------------|
| Operational Excellence | SRE, automation, observability | Cloud Operations, Cloud Deploy, Terraform |
| **Security** | Zero trust, org policies, encryption | IAM, Cloud KMS, VPC-SC, SCC, BeyondCorp |
| Reliability | Multi-region, SLOs, chaos | Load Balancing, Cloud Spanner, Backup DR |
| Performance Efficiency | Autoscaling, CDN, profiling | Cloud CDN, Recommender, Profiler |
| Cost Optimization | CUDs, rightsizing | Billing, Recommender, labels |
| Sustainability | Efficient regions, batch scheduling | Carbon-free energy regions |

**Review tool:** Security Command Center posture + Architecture Framework checklists

**Note:** GCP renamed “Well-Architected” to **Architecture Framework** — same six pillars.

→ Full Workload Identity/KMS/SCC: **`gcp-security-best-practices`**

---

## 5. Oracle Cloud Infrastructure (OCI)

**Docs:** [OCI Architecture Center](https://docs.oracle.com/en/solutions/oci-best-practices/)

| Pillar | OCI focus | Key services |
|--------|-----------|--------------|
| Operational Excellence | OCI Events, monitoring, Resource Manager | Logging Analytics, Alarms, OS Management |
| **Security** | Compartments, IAM, Security Zones | IAM, Vault, Cloud Guard, WAF, Data Safe |
| Reliability | ADs, DRG, Full Stack DR | Load Balancer, Autoscaling, Data Guard |
| Performance Efficiency | Shapes, caching | Autoscaling, CDN, HeatWave |
| Cost Optimization | Cost analysis, tagging | Cost Management, budgets |
| Sustainability | Efficient shapes, region choice | OCI sustainability reports |

**Review tool:** Cloud Guard + Security Zones compliance recipes + CIS OCI Benchmark

→ Full resource principal/Vault/VCN: **`oci-oracle-cloud-security`**

---

## 6. IBM Cloud (formerly Bluemix)

**Legacy names:** **IBM Bluemix** (PaaS brand, 2014–2019) → **IBM Cloud**; **IBM Cloud Foundry** enterprise → often on **Tanzu** or **Code Engine** today.

**Docs:**

- [IBM Cloud Security and Compliance Center](https://www.ibm.com/products/security-and-compliance-center)
- [IBM Cloud Framework for Financial Services](https://www.ibm.com/cloud/compliance/financial-services) (gold standard for regulated WAF-style controls)
- IBM Garage **Well-Architected** workshops (hybrid cloud)

| Pillar | IBM Cloud focus | Key services |
|--------|-----------------|--------------|
| Operational Excellence | Activity Tracker, Monitoring | Log Analysis, Schematics, Cloud Pak integrations |
| **Security** | Access groups, HPCS, posture | IAM, Key Protect/HPCS, Secrets Manager, SCC |
| Reliability | Multi-zone, HA pairs | Load Balancer, Backup, PostgreSQL HA |
| Performance Efficiency | Right-sizing, Code Engine scale | VSI profiles, IKS autoscale |
| Cost Optimization | Cost estimates, reservations | IBM Cloud billing tools |
| Sustainability | Efficient datacenters | IBM env reporting |

**Review tool:** **Security and Compliance Center (SCC)** — profiles for ISO, SOC, PCI, CIS; **Activity Tracker** evidence

**Bluemix migration note:** map legacy Bluemix org/space → IBM Cloud resource groups; Cloud Foundry on Bluemix → **Tanzu Application Service** or **Code Engine**; use **`ibm-cloud-security-best-practices`** + **`vmware-tanzu-pcf-security`** if CF remains.

→ Full Trusted Profile/HPCS: **`ibm-cloud-security-best-practices`**

---

## 7. Alibaba Cloud Well-Architected Framework

**Docs:** [Alibaba Cloud Well-Architected Framework](https://www.alibabacloud.com/help/en/well-architected)

| Pillar | Alibaba focus | Key services |
|--------|---------------|--------------|
| Operational Excellence | ActionTrail, CMS, OOS | Log Service, ARMS, OOS |
| **Security** | RAM, KMS, Security Center | RAM, KMS, WAF, Cloud Firewall, Security Center |
| Reliability | Multi-zone, ASR | SLB, ESS, HA across zones |
| Performance Efficiency | Auto Scaling, CDN | ESS, CDN, DCDN |
| Cost Optimization | Cost analysis, SP | Cost Management, resource tagging |
| Sustainability | Green datacenter initiatives | Region/carbon awareness |

**Review tool:** Security Center compliance check + Well-Architected online assessment

→ Full RAM/KMS/ActionTrail: **`alibaba-cloud-security-best-practices`**

---

## 8. VMware Tanzu / Pivotal Cloud Foundry (PCF)

**Legacy names:** **Pivotal Cloud Foundry (PCF)** → **VMware Tanzu Application Service (TAS)**; **Pivotal Web Services (PWS)** → discontinued; often deployed on AWS/Azure/GCP/vSphere.

**Docs:**

- [VMware Tanzu Reference Architecture](https://docs.vmware.com/en/VMware-Tanzu/index.html)
- [Tanzu Application Service security](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/index.html)

PCF/Tanzu does not ship a branded “Well-Architected Tool” like AWS. Reviews use:

| Pillar | Tanzu / PCF focus | Key components |
|--------|-------------------|----------------|
| Operational Excellence | BOSH, Ops Manager, Healthwatch | Loggregator, Metrics, stemcell lifecycle |
| **Security** | UAA, CredHub, ASGs, isolation | UAA/OAuth, CredHub, ASGs, Isolation Segments, NSX-T |
| Reliability | Diego HA, multi-AZ, DB tiles | BOSH HA, singleton vs HA job templates |
| Performance Efficiency | Diego cell sizing, routing | Gorouter, autoscaling apps, TKG HPA |
| Cost Optimization | Cell capacity, foundation sizing | Right-size Diego cells, shared services org |
| Sustainability | Underlying IaaS choice | Apply AWS/Azure/GCP sustainability pillar |

**Review approach:** map to **NIST CSF** + underlying **IaaS WAF** (AWS/Azure/GCP skill) + **`vmware-tanzu-pcf-security`**

**Pivotal-era checklist:** UAA → CredHub → ASGs → stemcells → audit events (same in Tanzu).

→ Full UAA/CredHub/ASG: **`vmware-tanzu-pcf-security`**

---

## 9. Cross-cloud Security pillar — unified control map

Use this for “one question, all clouds” workshops. Detail in [references/well-architected-pillar-matrix.md](references/well-architected-pillar-matrix.md).

| Security principle | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------------------|-----|-------|-----|-----|-------------|---------|-----------|
| Human SSO + MFA | IAM Identity Center | Entra ID + CA | Cloud Identity / IdP | Federated IAM | IBMid | RAM federated | UAA SAML |
| Workload identity | IAM role / IRSA | Managed identity | Workload Identity | Resource principal | Trusted Profile | ECS RAM / RRSA | UAA client / K8s SA |
| Secrets vault | Secrets Manager | Key Vault | Secret Manager | OCI Vault | Secrets Manager | Secrets Manager | CredHub |
| Encryption keys | KMS | Key Vault keys | Cloud KMS | Vault keys | Key Protect/HPCS | KMS | CredHub + cloud KMS |
| Network zero trust | VPC + SG + WAF | VNet + NSG + WAF | VPC + firewall + Armor | VCN + NSG + WAF | VPC SG + CIS | VPC + Cloud Firewall | ASG + network policy |
| Audit trail | CloudTrail | Activity Log | Audit Logs | Audit service | Activity Tracker | ActionTrail | CF audit events |
| Threat detection | GuardDuty | Defender | SCC | Cloud Guard | SCC | Security Center | IaaS + platform logs |
| Posture management | Security Hub | Defender CSPM | SCC | Cloud Guard | SCC | Security Center | Underlying IaaS WAF |

---

## 10. How to run a multi-cloud WAF review (this repo)

### Step 1 — Select frameworks
Load this skill + `multi-cloud-security-posture`.

### Step 2 — Per workload
1. Identify hosting cloud (or PCF on IaaS)
2. Open provider WAF docs (section 2–8 above)
3. Load matching **cloud skill** for IAM/KMS/logging depth
4. Score each pillar 0–3 (0 = missing, 3 = automated + tested)

### Step 3 — Security pillar (mandatory depth)
- Identity: no static keys (`zero-trust-identity-and-secrets`)
- Encryption: CMK at rest, TLS in transit
- Detection: org-wide audit + CSPM
- Agent/MCP: Bastion proxy + AIV gate

### Step 4 — Deliverables
- High-risk gaps (Security + Reliability first)
- Remediation mapped to cloud skill sections
- Re-review in provider tool (WA Tool, SCC, Security Center, etc.)

---

## 11. Official review tools quick reference

| Cloud | Tool | URL pattern |
|-------|------|-------------|
| AWS | Well-Architected Tool | AWS Console → Well-Architected Tool |
| Azure | WAF review + Advisor | learn.microsoft.com/azure/well-architected |
| GCP | Architecture Framework + SCC | cloud.google.com/architecture/framework |
| OCI | Cloud Guard + CIS benchmark | OCI Console → Cloud Guard |
| IBM / Bluemix | SCC profiles | IBM Cloud → Security and Compliance Center |
| Alibaba | Well-Architected assessment | Alibaba Cloud console → Well-Architected |
| PCF / Tanzu | Manual + IaaS WA Tool | Tanzu docs + underlying cloud WA Tool |

---

## 12. Verification checklist

- [ ] All in-scope clouds identified (including Bluemix/PCF legacy names)
- [ ] All six pillars scored per workload
- [ ] Security pillar mapped using section 9 table
- [ ] Provider review tool selected and export saved
- [ ] Matching cloud skill loaded for each provider
- [ ] PCF/Tanzu reviews include underlying IaaS WAF
- [ ] Agent workloads checked against zero-trust skill

---

## 13. Red flags

- Reviewing only Security pillar and ignoring Reliability/Cost (WAF is holistic)
- Treating Bluemix as separate from IBM Cloud IAM/SCC
- PCF review without CredHub/UAA and without IaaS layer
- Using AWS WA Tool questions verbatim on Azure without mapping
- No exported evidence from official review tool for audit

---

## Related skills

- `multi-cloud-security-posture` — unified 12-domain baseline
- `using-cloud-security-agent-skills` — session routing
- `zero-trust-identity-and-secrets` — identity across all clouds
- All seven cloud skills (AWS, Azure, GCP, OCI, IBM, Alibaba, PCF)
- [references/well-architected-pillar-matrix.md](references/well-architected-pillar-matrix.md) — full cross-cloud matrix
