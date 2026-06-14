---
name: using-cloud-security-agent-skills
description: Start here — end-to-end routing for multi-cloud security agent work. Meta skills, per-cloud IAM/KMS/network/logging depth (AWS/Azure/GCP/OCI/IBM/Alibaba/PCF), Bastion, mcp-test, AIV gate, lifecycle, and verification.
---

# Using Cloud Security Agent Skills

## Overview

**cloud-security-agent-skills** is a **specialized security-only** repository. All **14 skills** live in `skills/` — no external skill repos. Each cloud skill is **end-to-end**: IAM → KMS/vault → network → compute → data → logging → detection → compliance → checklists.

**One-stop Well-Architected:** `cloud-well-architected-frameworks` — AWS/Azure/GCP/OCI/IBM Bluemix/Alibaba/PCF six pillars in one place.

**Stack:** zero-trust identity → cloud best practices → Bastion → MCP test harness → AIV gate.

---

## When to use this repo

- AWS/Azure/GCP/OCI/IBM/Alibaba/PCF security assessment or hardening
- Agent deployment review (IRSA, managed identity, resource principal, etc.)
- MCP client hardening with Bastion
- PR security validation, adversarial MCP testing
- WAF / Well-Architected review across any cloud (AWS, Azure, GCP, OCI, IBM Bluemix, Alibaba, PCF/Tanzu)
- Hybrid or unknown cloud — multi-cloud baseline first

---

## 1. Session start (mandatory order)

### Step 1 — Meta layer

| Skill | Purpose |
|-------|---------|
| **`cloud-well-architected-frameworks`** | **One-stop WAF** — all clouds, six pillars, Bluemix/PCF legacy mapping |
| **`zero-trust-identity-and-secrets`** | No static keys; IdentityManager; secret lifecycle |
| **`multi-cloud-security-posture`** | Unified 12-domain baseline; hybrid routing |

### Step 2 — Primary cloud skill (one per cloud in scope)

| Cloud | Skill | Covers (end-to-end) |
|-------|-------|---------------------|
| AWS | `aws-security-best-practices` | Orgs/SCP, IAM/SSO/IRSA, KMS, VPC/WAF, EKS, S3/RDS, CloudTrail/GuardDuty/Config/Security Hub, CIS/compliance |
| Azure | `azure-security-best-practices` | Entra ID/CA/PIM, Key Vault, hub-spoke, Defender, Purview, Sentinel |
| GCP | `gcp-security-best-practices` | Org policies, VPC-SC, Workload Identity, Cloud KMS/CMEK, GKE, SCC |
| OCI | `oci-oracle-cloud-security` | IAM/compartments, Vault, VCN/NSG, Cloud Guard, Security Zones, Data Safe |
| IBM / Bluemix | `ibm-cloud-security-best-practices` | IAM/access groups, Trusted Profile, Key Protect/HPCS, Activity Tracker, SCC |
| Alibaba | `alibaba-cloud-security-best-practices` | RAM/STS, KMS, VPC, ActionTrail, Security Center |
| PCF / Pivotal / Tanzu | `vmware-tanzu-pcf-security` | UAA, CredHub, ASG, network policies, BOSH, TKG/Istio |

Each skill has **verification checklist** and **red flags**. Optional deep checklist: `skills/<skill>/references/end-to-end-checklist.md`.

### Step 3 — Tooling layer

| Skill | Tool |
|-------|------|
| `mcp-bastion-security-gateway` | `bastion.yaml`, proxy, PII/injection defense |
| `mcp-security-testing-harness` | Protocol + adversarial MCP tests |
| `pr-integrity-aiv-gate` | PR density, design rules, invariants |

---

## 2. Security lifecycle

```
/assess  → posture + cloud skill checklists
/harden  → remediate gaps (IAM, KMS, network, logging)
/validate → mcp-test security suite + manual review
/gate    → AIV on PR (no static keys, no MCP bypass)
/monitor → CSPM, SIEM, GuardDuty/Defender/SCC continuous
```

---

## 3. In-repo components

| Path | Role |
|------|------|
| `security/` | `IdentityManager` ABC + 7 cloud managers + introspection |
| `agent/` | `CloudSecurityAgent`, Bastion gateway/proxy/wrapper, MCP server |
| `bastion.yaml` | PromptGuard, Presidio, rate limits, RBAC |
| `mcp-test.yaml` | Harness config |
| `.aiv/` | PR integrity gate |
| `tests/` | Unit + integration (protocol + security) |

### CLI

```bash
cloud-security-agent          # posture + skills status
mcp-bastion validate --config bastion.yaml
mcp-test --transport stdio --server-command "python -m agent.mcp_server"
pytest tests/unit/
```

Expected: `skills_complete: true`, `available_count: 14`

---

## 4. MCP client configuration (required)

Never connect directly to `agent.mcp_server`. Always:

```json
{
  "command": "python",
  "args": ["-m", "agent.bastion_proxy", "--", "python", "-m", "agent.mcp_server"]
}
```

---

## 5. Identity by cloud (agent deployments)

| Cloud | Mechanism | Never use |
|-------|-----------|-----------|
| AWS | IRSA / instance profile | Access keys |
| Azure | Managed identity | Client secret on compute |
| GCP | Workload Identity | Downloaded SA JSON key |
| OCI | Resource principal | API signing key in code |
| IBM | Trusted Profile | Service ID API key |
| Alibaba | ECS RAM role / RRSA | AccessKey in env |
| PCF | UAA + CredHub | Secrets in manifest.yml |

See `zero-trust-identity-and-secrets` for code patterns.

---

## 6. What "nothing missed" means per cloud skill

Every cloud skill includes these sections:

1. Org/account/compartment governance  
2. **IAM** (humans, workloads, policies, anti-patterns)  
3. **KMS / vault / secrets** (encryption matrix)  
4. **Network** (segmentation, private link, WAF, flow logs)  
5. **Compute / Kubernetes** (hardening, pod identity)  
6. **Data services** (object storage, databases)  
7. **Logging & audit** (org trail, SIEM)  
8. **Detection & CSPM** (GuardDuty, Defender, SCC, etc.)  
9. **Compliance** (CIS, regulatory mapping)  
10. **Agent/MCP** on that cloud  
11. **Verification checklist**  
12. **Red flags**

---

## 7. Red flags (stop and fix)

- Static credentials in code or committed config
- MCP client bypasses `agent.bastion_proxy`
- Cloud review without loading matching cloud skill
- PR merged without AIV + Bastion validation
- Skipping KMS/vault section in assessment
- Public object storage or database endpoint

---

## 8. Verification checklist

- [ ] Meta skills loaded (`zero-trust`, `multi-cloud` if hybrid)
- [ ] Primary cloud skill loaded for each in-scope cloud
- [ ] Tooling skills referenced for MCP/PR work
- [ ] `cloud-security-agent` → `skills_complete: true`
- [ ] `mcp-bastion validate` passes
- [ ] No secret literals in current diff

---

## Related documentation

- [skills-index.md](../../skills-index.md) — full catalog
- [AGENTS.md](../../AGENTS.md) — agent routing
- [docs/folder-structure.md](../../docs/folder-structure.md) — repo map
