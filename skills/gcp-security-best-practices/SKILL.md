---
name: gcp-security-best-practices
description: End-to-end GCP security — Organization, IAM, Workforce/Workload Identity Federation, VPC SC, Cloud KMS, Secret Manager, Cloud Armor, SCC, Chronicle, Cloud Logging, GKE hardening, CMEK, and zero service account keys.
---

# GCP Security Best Practices (End-to-End)

## Overview

Full-stack GCP security for projects, folders, GKE agents, and data platforms. Use **Application Default Credentials** via `GCPDefaultCredentialManager` — **never download JSON service account keys**.

---

## 1. Resource hierarchy and organization policies

### Hierarchy

- **Organization** → **Folders** (prod, nonprod, shared, security) → **Projects**
- **Separate projects** for: networking hub, security tooling, prod workloads, nonprod, billing export
- **Labels** mandatory: `environment`, `data_class`, `owner`, `cost_center`

### Organization policies (enforce at org/folder)

| Constraint | Purpose |
|------------|---------|
| `iam.disableServiceAccountKeyCreation` | No SA keys |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | Disable default SA over-permission |
| `compute.requireVpcFlowLogs` | Flow logs on subnets |
| `compute.vmExternalIpAccess` | Deny external IPs on VMs |
| `storage.publicAccessPrevention` | No public buckets |
| `gcp.restrictNonCmekServices` | CMEK-only for listed services |
| `constraints/gcp.restrictVPCPeering` | Control peering |
| `sql.restrictPublicIp` | Cloud SQL private only |

### VPC Service Controls

- **Access policies** with perimeters around projects handling sensitive data (BigQuery, GCS, Secret Manager)
- **Ingress/egress policies** for hybrid and multi-project access
- **Dry-run mode** before enforce; break-glass procedure documented

---

## 2. Identity and access management (IAM)

### Humans

- **Google Workspace / Cloud Identity** sync; **2SV enforced** for all users
- **Organization custom roles** instead of primitive `roles/owner` for daily ops
- **Just-in-time access** via Entitlement Management or third-party PAM where required
- **Admin activity audit logs** exported and alerted

### Workloads

- **Workload Identity Federation** — AWS/Azure/GitHub/OIDC to GCP without keys
- **GKE Workload Identity** — `serviceAccount:PROJECT.svc.id.goog[NAMESPACE/KS SA]` binding
- **Service accounts** — one per microservice; no `roles/editor` or `roles/owner` on SA
- **Service account impersonation** restricted; audit `iam.serviceAccounts.getAccessToken`

### IAM best practices

- **Deny policies** (IAM Deny) for break-glass separation
- **Conditional IAM** — `resource.name`, `request.time`, `iam.googleapis.com/resourceTags`
- **Policy Intelligence** — recommender for unused permissions; trim quarterly
- **Key rotation** N/A for keys you don't create — enforce key creation org policy

---

## 3. Cloud KMS and encryption

### Cloud KMS

- **Key rings** per environment/region; **HSM** keys for regulated data
- **Separation of duties**: key admin ≠ key user ≠ crypto operator
- **Rotation period** set on keys; automated rotation for symmetric keys
- **EKM** (External Key Manager) for BYOK/HYOK requirements

### CMEK coverage

| Service | CMEK |
|---------|------|
| GCS buckets | Cloud KMS key on bucket |
| BigQuery | Dataset default encryption |
| Pub/Sub | Topic CMEK |
| GCE disks | Disk encryption key |
| Cloud SQL | CMEK instance setting |
| GKE etcd secrets | Application-layer secrets + KMS |
| Secret Manager | Customer-managed encryption keys |

### In transit

- **TLS 1.2+** on HTTPS load balancers; modern cipher profiles
- **Certificate Manager** / managed certs; monitor expiry

---

## 4. Network security

### VPC design

- **Shared VPC** — host project for network; service projects attach
- **Private Google Access** on subnets for API reachability without external IP
- **Cloud NAT** for controlled egress with logging
- **VPC Flow Logs** — 5-tuple sampling; export to BigQuery/SCC

### Firewall

- **Hierarchical firewall policies** at org/folder
- **Network firewall policies** — default deny ingress; tag-based targeting
- **No `0.0.0.0/0` on SSH/RDP** except documented bastion with IAP

### Identity-Aware Proxy (IAP)

- **IAP TCP forwarding** for admin access without public SSH
- **IAP for HTTPS** on internal apps; Entra/OIDC integration via BeyondCorp

### Edge

- **Cloud Armor** — WAF rules, rate limiting, geo restrictions, adaptive protection
- **Cloud CDN** signed URLs for sensitive static assets
- **Private Service Connect** for Google APIs and published services

---

## 5. GKE and containers

- **Private cluster** — private nodes, control plane authorized networks or private endpoint
- **Workload Identity** enabled; disable legacy metadata server exposure
- **Binary Authorization** — only signed images deploy (Attestor + GKE policy)
- **GKE Sandbox (gVisor)** for untrusted workloads optional
- **Network Policies** default deny; Calico/Cilium
- **Shielded GKE nodes** — secure boot, integrity monitoring
- **Vulnerability scanning** — Artifact Analysis on Artifact Registry
- **Pod Security Standards** enforced via admission

---

## 6. Data services

### Cloud Storage

- **Uniform bucket-level access**; no ACLs
- **Public access prevention** org policy
- **Bucket Lock** / retention policies for compliance
- **Object versioning** + lifecycle to Nearline/Coldline with encryption

### BigQuery

- **Dataset IAM** + authorized views; column-level security / policy tags
- **Audit logs** for data access; **DLP API** inspection jobs
- **Row access policies** for multi-tenant

### Cloud SQL / Spanner / AlloyDB

- Private IP only; **IAM DB auth** where supported
- Automated backups encrypted; PITR enabled
- SSL required for connections

---

## 7. Secrets

- **Secret Manager** — versioning, IAM on secrets, CMEK
- **No secrets in Cloud Build substitutions** plain text — use Secret Manager refs
- **No SA keys in Git** — org policy + Secret Scanner

---

## 8. Logging, monitoring, and detection

| Log | Export |
|-----|--------|
| Admin Activity | Non-configurable; also export |
| Data Access | Enable for Storage, BigQuery, KMS — **critical** |
| VPC Flow | BigQuery / Chronicle |
| Firewall | Cloud Logging |
| Cloud Audit + SIEM | Pub/Sub → Chronicle / Splunk |

- **Security Command Center Premium** — VM vulnerability, Event Threat Detection, container threat detection
- **Cloud Logging buckets** with retention locks for audit
- **Log sinks** immutable; separate project for security log archive
- **Uptime checks + alerting policies** on security tooling health

---

## 9. Compliance and governance

- **Assured Workloads** for FedRAMP/IL4/IL5 style requirements
- **Compliance monitoring** in SCC for CIS, PCI, NIST
- **Forseti/Config Validator** or **Policy Controller** (Anthos) for K8s/GCP policy

---

## 10. Agent / MCP on GCP

- GKE **Workload Identity** for agent SA; scopes minimal
- **VPC-SC** if agent accesses BigQuery/GCS with sensitive data
- Cloud Run: dedicated SA per service; ingress internal-only
- Bastion gateway on all MCP paths; rate limits in `bastion.yaml`

---

## 11. Verification checklist

- [ ] Org policy: disable SA key creation
- [ ] No downloadable SA keys in org (Asset Inventory scan)
- [ ] VPC-SC perimeters for sensitive projects
- [ ] CMEK on regulated buckets/datasets
- [ ] SCC Premium enabled
- [ ] Data access audit logs ON for Storage/BQ/KMS
- [ ] Cloud Armor on public L7 LB
- [ ] GKE private + workload identity + binary authorization

---

## 12. Red flags

- Service account JSON key in repo or VM disk
- Bucket `allUsers` ACL or IAM binding
- Cloud SQL public IP enabled
- Project `roles/owner` for default compute SA
- Missing data access audit logs on sensitive datasets

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected:** see `cloud-well-architected-frameworks` — Google Cloud Architecture Framework, six pillars.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
