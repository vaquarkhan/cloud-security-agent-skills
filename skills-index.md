# Skills index — cloud-security-agent-skills

**14 self-contained security skills** in `skills/`. No external repositories.

Each **cloud skill** is end-to-end: governance → **IAM** → **KMS/vault** → network → compute/K8s → data → logging → detection → compliance → agent/MCP → checklist → red flags.

Optional printable checklists: `skills/<name>/references/end-to-end-checklist.md`

---

## Meta and cross-cloud

| Skill | Purpose |
|-------|---------|
| `using-cloud-security-agent-skills` | **Start here** — session routing, lifecycle, component map |
| `cloud-well-architected-frameworks` | **One-stop WAF** — AWS/Azure/GCP/OCI/IBM Bluemix/Alibaba/PCF six pillars + cross-cloud matrix |
| `zero-trust-identity-and-secrets` | Ephemeral credentials, IdentityManager, secret lifecycle, forbidden patterns |
| `multi-cloud-security-posture` | 12-domain unified baseline, service mapping table, hybrid SIEM |

---

## Cloud security best practices (end-to-end)

| Skill | Cloud | Key domains |
|-------|-------|-------------|
| `aws-security-best-practices` | Amazon Web Services | Orgs/SCP, IAM/SSO/IRSA, KMS, VPC/WAF, EKS, S3/RDS, CloudTrail/GuardDuty/Config/Security Hub |
| `azure-security-best-practices` | Microsoft Azure | Entra ID/CA/PIM, Key Vault, hub-spoke, Defender, Purview, Sentinel |
| `gcp-security-best-practices` | Google Cloud Platform | Org policies, VPC-SC, Workload Identity, Cloud KMS/CMEK, GKE, SCC |
| `oci-oracle-cloud-security` | Oracle Cloud Infrastructure | IAM/compartments, Vault, VCN/NSG, Cloud Guard, Security Zones, Data Safe |
| `ibm-cloud-security-best-practices` | IBM Cloud | Access groups, Trusted Profile, Key Protect/HPCS, Activity Tracker, SCC |
| `alibaba-cloud-security-best-practices` | Alibaba Cloud | RAM/STS, KMS, VPC, ActionTrail, Security Center |
| `vmware-tanzu-pcf-security` | VMware Tanzu / Cloud Foundry | UAA, CredHub, ASG, network policies, BOSH, TKG/Istio |

---

## Tooling layer

| Skill | Tool |
|-------|------|
| `mcp-bastion-security-gateway` | MCP-Bastion — `bastion.yaml`, proxy, PII/injection |
| `mcp-security-testing-harness` | mcp-test-harness — protocol + adversarial tests |
| `pr-integrity-aiv-gate` | AIV gate — `.aiv/` design rules |

---

## Verify installation

```bash
cloud-security-agent
# skills_complete: true
# available_count: 14
```

```bash
mcp-bastion validate --config bastion.yaml
pytest tests/unit/
```

---

## Skill structure convention

Every cloud `SKILL.md` includes:

1. Governance / org structure  
2. IAM (humans + workloads + anti-patterns)  
3. KMS / vault / encryption matrix  
4. Network (segmentation, WAF, flow logs)  
5. Compute / Kubernetes  
6. Data protection (object storage, databases)  
7. Logging, audit, SIEM  
8. Detection / CSPM  
9. Compliance (CIS, regulatory)  
10. Agent / MCP deployment on that cloud  
11. Verification checklist  
12. Red flags  

See also [AGENTS.md](AGENTS.md) and [docs/folder-structure.md](docs/folder-structure.md).
