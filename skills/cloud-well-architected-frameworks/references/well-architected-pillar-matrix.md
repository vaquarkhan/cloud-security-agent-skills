# Well-Architected Pillar Matrix — All Clouds

One reference table for architecture reviews. Pair with `cloud-well-architected-frameworks` skill and per-cloud security skills.

**Legacy platform names:** Bluemix → IBM Cloud | Pivotal Cloud Foundry (PCF) → VMware Tanzu Application Service (TAS)

---

## Framework names and documentation

| Provider | Official framework | Primary doc |
|----------|-------------------|-------------|
| AWS | AWS Well-Architected Framework | https://docs.aws.amazon.com/wellarchitected/latest/framework/ |
| Azure | Microsoft Azure Well-Architected Framework | https://learn.microsoft.com/en-us/azure/well-architected/ |
| GCP | Google Cloud Architecture Framework | https://cloud.google.com/architecture/framework |
| OCI | OCI Architecture Center / Best Practices | https://docs.oracle.com/en/solutions/oci-best-practices/ |
| IBM Cloud (Bluemix) | IBM Cloud Framework + SCC profiles; Financial Services Framework | https://www.ibm.com/cloud/compliance/financial-services |
| Alibaba | Alibaba Cloud Well-Architected Framework | https://www.alibabacloud.com/help/en/well-architected |
| VMware Tanzu (PCF) | Tanzu Reference Architecture + NIST CSF (no single WA Tool) | https://docs.vmware.com/en/VMware-Tanzu/ |

---

## Pillar 1 — Operational Excellence

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| IaC | CloudFormation, CDK, Terraform | Bicep, ARM, Terraform | Deployment Manager, Terraform | Resource Manager, Terraform | Schematics, Terraform | ROS, Terraform | BOSH manifests, Terraform (IaaS) |
| CI/CD | CodePipeline, CodeBuild | Azure DevOps, GitHub Actions | Cloud Build, Cloud Deploy | DevOps CI/CD | Tekton, DevOps Insights | Flow, DevOps | Concourse (Tanzu), CF push pipelines |
| Observability | CloudWatch, X-Ray | Monitor, App Insights | Cloud Operations, Trace | Logging Analytics, APM | Log Analysis, Instana | ARMS, SLS | Loggregator, Healthwatch, Tanzu Observability |
| Runbooks | Systems Manager | Automation, Runbooks | Cloud Functions automation | OOS | Automation | OOS | BOSH errand docs, runbooks |
| Change mgmt | Change Manager | Safe Deployments | Cloud Deploy canaries | Resource Manager stacks | Change Management | CMS change tracking | Ops Manager tile upgrades |
| Agent ops | SSM, EventBridge | Automation | Cloud Scheduler | Events | Cloud Functions | FC scheduled | CF app health checks |

---

## Pillar 2 — Security (expanded)

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| Human IAM | IAM Identity Center | Entra ID, PIM | Cloud Identity | IAM + federation | IBMid, access groups | RAM users + MFA | UAA + IdP SAML |
| Workload IAM | IAM roles, IRSA | Managed identity, WIF | Workload Identity | Resource principal | Trusted Profile | ECS RAM, RRSA | UAA client, K8s SA |
| Key mgmt | KMS | Key Vault | Cloud KMS | OCI Vault | Key Protect, HPCS | KMS | CredHub + cloud KMS |
| Secrets | Secrets Manager | Key Vault secrets | Secret Manager | Vault secrets | Secrets Manager | Secrets Manager | CredHub, UPS bindings |
| Network | VPC, SG, NACL, WAF | VNet, NSG, Azure Firewall, WAF | VPC, firewall, Armor | VCN, NSG, WAF | VPC SG, CIS WAF | VPC, Cloud Firewall, WAF | ASG, Isolation Segment, NSX-T |
| Data at rest | SSE-KMS, EBS, RDS TDE | Storage SSE, SQL TDE | CMEK, default encryption | Vault encryption | KP/HPCS encryption | KMS OSS/RDS | BOSH disk + blobstore SSE |
| Data in transit | TLS, ACM | TLS, App Gateway | TLS, Certificate Manager | TLS certs | TLS | TLS | Gorouter TLS, service tile TLS |
| Audit | CloudTrail org | Activity Log, Diagnostic settings | Admin/Data Access logs | Audit service | Activity Tracker | ActionTrail | CF audit events |
| CSPM | Security Hub, Config | Defender for Cloud | Security Command Center | Cloud Guard | SCC | Security Center | IaaS CSPM + platform audit |
| Threat detect | GuardDuty, Macie | Defender plans | SCC Premium, Chronicle | Cloud Guard | Guardium, SCC | Security Center | SIEM on logs |
| App security | WAF, Shield, Inspector | WAF, Defender for App | Web Security Scanner | WAF | App ID (legacy Bluemix) | WAF | Route services, container scan |
| Agent/MCP | IRSA + Bastion | MI + Bastion | WIF + Bastion | Resource principal + Bastion | Trusted Profile + Bastion | RAM role + Bastion | UAA + Bastion |

**Repo deep-dives:** `aws-security-best-practices`, `azure-security-best-practices`, `gcp-security-best-practices`, `oci-oracle-cloud-security`, `ibm-cloud-security-best-practices`, `alibaba-cloud-security-best-practices`, `vmware-tanzu-pcf-security`

---

## Pillar 3 — Reliability

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| Multi-AZ | AZs, Auto Scaling | Availability Zones | Zones, regional LB | Availability Domains | Zones | Zones | Multi-AZ Diego, TKG nodes |
| DR | Backup, DR sites, Route 53 | Site Recovery, paired regions | Backup DR, multi-region | Full Stack DR, Data Guard | Backup, cross-region COS | Cross-region replication | Foundation DR, blobstore replication |
| Health checks | ELB, Route 53 | Load Balancer, Traffic Manager | Load Balancing health checks | LB health checks | LB health checks | SLB health checks | Gorouter health, BOSH health monitors |
| Quotas | Service Quotas | Subscription limits | Quotas | Limits | Quotas | Quotas | Cell capacity, Doppler limits |
| Chaos / test | FIS | Chaos Studio (preview) | Fault Injection (GKE) | Chaos tools (3rd party) | Gremlin integrations | AHAS | CF chaos experiments (custom) |
| Backup | AWS Backup | Azure Backup | Backup and DR | Block/db backup | Backup | HBR | BOSH persistent disk backup |

---

## Pillar 4 — Performance Efficiency

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| Right-sizing | Compute Optimizer | Advisor | Recommender | Shape analysis | VSI sizing | CMS recommendations | Diego cell sizing |
| Autoscale | ASG, Lambda | VMSS, App Service | MIG, GKE HPA | Autoscaling | IKS HPA, Code Engine | ESS, ACK HPA | App autoscaling, TKG HPA |
| CDN | CloudFront | Front Door, CDN | Cloud CDN | CDN | CIS CDN | CDN, DCDN | CloudFront/FD in front of Gorouter |
| Caching | ElastiCache | Azure Cache | Memorystore | Redis service | Databases for Redis | ApsaraDB Redis | Redis service tile |
| Serverless | Lambda | Functions | Cloud Run, Functions | Functions | Code Engine, CF | FC, SAE | Cloud Functions on CF (legacy) |
| GPU/HPC | EC2 GPU, Trainium | NC-series | TPU, GPU VMs | GPU shapes | GPU profiles | GPU instances | N/A typical |

---

## Pillar 5 — Cost Optimization

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| Visibility | Cost Explorer, CUR | Cost Management | Billing, labels | Cost analysis | IBM Cloud billing | Cost Management | CloudHealth, underlying CUR |
| Commitments | RI, Savings Plans | Reservations | CUDs | UCM | Reserved instances | RI/SCU | IaaS RIs under foundation |
| Tagging | Cost allocation tags | Tags | Labels | Freeform/defined tags | Tags | Tags | Org/space labels, CF tags |
| Idle resources | Trusted Advisor | Advisor | Recommender | Cost reports | Idle resource reports | CMS | Unused apps, over-sized cells |
| Architect review | WA Cost questions | WAF Cost pillar | Framework cost section | OCI cost guides | Garage cost workshops | WA cost section | Foundation sizing review |

---

## Pillar 6 — Sustainability

| Topic | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|-------|-----|-------|-----|-----|-------------|---------|-----------|
| Carbon reporting | Customer Carbon Footprint Tool | Emissions Impact Dashboard | Carbon-aware regions | Sustainability reports | Env reports | Green initiatives | Use IaaS provider tool |
| Efficient compute | Graviton, Inferentia | Azure efficient VMs | Tau T2A, custom silicon | Ampere shapes | Power-efficient profiles | g8i etc. | Right-size cells |
| Region choice | Renewable regions | Low-carbon regions | CFE regions | Region selection | Region selection | Region selection | IaaS region selection |
| Scheduling | Stop dev instances | DevTest Labs auto-shutdown | Scheduler | OOS schedules | Code Engine scale-to-zero | Scheduled scaling | Scale-to-zero apps |

---

## Bluemix → IBM Cloud migration mapping

| Bluemix (legacy) | IBM Cloud (current) | Tanzu / alternative |
|----------------|---------------------|---------------------|
| Bluemix org / space | Resource groups + account | CF org/space on TAS |
| Bluemix IAM | IBM Cloud IAM access groups | Same |
| App ID | Verify / CIS + custom IdP | UAA on TAS |
| Cloud Foundry on Bluemix | IBM Cloud Foundry (deprecated paths) | VMware Tanzu Application Service |
| Compose databases | IBM Cloud Databases | Managed DB services |
| Bluemix API keys | Eliminate → Trusted Profile | UAA + CredHub |

---

## PCF / Pivotal → Tanzu mapping

| Pivotal / PCF (legacy) | VMware Tanzu (current) |
|------------------------|------------------------|
| Pivotal Cloud Foundry (PCF) | Tanzu Application Service (TAS) |
| Pivotal Application Service | TAS |
| Pivotal Web Services (PWS) | Discontinued — migrate to TAS or public cloud |
| PKS (Pivotal Container Service) | Tanzu Kubernetes Grid (TKG) |
| Ops Manager | Ops Manager (Tanzu) |
| CredHub | CredHub |
| UAA | UAA |
| Isolation Segment | Isolation Segment (NSX-T) |

---

## WAF review scoring template

Score each pillar **0–3** per workload:

| Score | Meaning |
|-------|---------|
| 0 | Not addressed |
| 1 | Ad hoc / manual only |
| 2 | Documented + partially automated |
| 3 | Automated, tested, monitored, evidence exported |

**Priority order for security agents:** Security (2) → Reliability (3) → Operational Excellence (1) → Performance (4) → Cost (5) → Sustainability (6)

---

## Links to repo checklists

- AWS: `skills/aws-security-best-practices/references/end-to-end-checklist.md`
- Azure: `skills/azure-security-best-practices/references/end-to-end-checklist.md`
- GCP: `skills/gcp-security-best-practices/references/end-to-end-checklist.md`
- OCI: `skills/oci-oracle-cloud-security/references/end-to-end-checklist.md`
- IBM: `skills/ibm-cloud-security-best-practices/references/end-to-end-checklist.md`
- Alibaba: `skills/alibaba-cloud-security-best-practices/references/end-to-end-checklist.md`
- PCF/Tanzu: `skills/vmware-tanzu-pcf-security/references/end-to-end-checklist.md`
