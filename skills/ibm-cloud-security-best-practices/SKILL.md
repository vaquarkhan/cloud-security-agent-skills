---
name: ibm-cloud-security-best-practices
description: End-to-end IBM Cloud security — IAM access groups, Trusted Profile, ContainerAuthenticator, Key Protect/HPCS, Secrets Manager, Activity Tracker, SCC, VPC security groups, Private Path, and zero API keys for agents.
---

# IBM Cloud Security Best Practices (End-to-End)

## Overview

Full IBM Cloud security reference. Agents use **Trusted Profile** + `ContainerAuthenticator` (`TRUSTED_PROFILE_NAME` only) — no API keys in code.

---

## 1. Account and enterprise structure

- **Enterprise** (if licensed) with account groups: Production, Staging, Development, Security
- **Account separation** — prod workloads isolated from sandbox; shared services account for logging/SCC
- **Account settings** — enforce MFA for all users; restrict classic infrastructure if unused
- **Resource groups** per application/environment within account
- **Tagging** strategy: `env`, `data_class`, `owner`, `app`

---

## 2. Identity and access management (IAM)

### Human users

- **IBMid** with **MFA** mandatory for all users
- **Access groups** — not direct service ID/user policy attachment at scale
- **Custom roles** when viewer/editor too broad
- **Dynamic rules** for access groups (e.g., attribute-based from corporate IdP)

### Service IDs and trusted profiles

- **Service IDs** for automation — attach to access groups; **no API keys** where Trusted Profile works
- **Trusted Profile** for compute (Code Engine, IKS, VSI, Cloud Functions):
  - Profile links compute identity to service ID permissions
  - **Agent:** `TRUSTED_PROFILE_NAME` env injected by platform
- **IAM API keys** — eliminate for workloads; if legacy: rotate 90d, IP restrict, store in Secrets Manager

### Least privilege patterns

```
Access group: prod-object-storage-readers
  → Reader on specific bucket instance
Access group: agent-secrets-readers
  → Secrets Manager read on named secrets only
```

- **Activity Tracker** alerts on `iam.policy.create`, `iam.apiKey.create`

---

## 3. Key Protect and Hyper Protect Crypto Services (HPCS)

### Key Protect / HPCS

- **Root of trust** in HPCS for regulated workloads (FIPS 140-2 Level 3 HSM)
- **Dual authorization** for key deletion/disable
- **Key rotation** — import new key material or rotate CRK per policy
- **Envelope encryption** for Object Storage, Block Storage, databases

### Secrets Manager

- **Secrets** for credentials, API tokens, certificates
- **Automatic rotation** via Functions/Schematics where supported
- **IAM** scoped to secret groups; audit `secrets-manager.secret.read`

---

## 4. Network security

### VPC generation 2

- **Custom routes** — default route to VPN/Fortigate/Transit Gateway, not open internet
- **Security groups** — stateful rules; default deny inbound
- **No public interfaces** on databases or internal microservices
- **Public Gateway** only on subnets that require outbound internet; prefer **VPC endpoints** / **Private Path**

### Private Path

- **Private Path** for IBM Cloud services (COS, databases) without public internet traversal
- **Direct Link / VPN** for hybrid with encryption (IPsec/IKEv2)

### Edge

- **Cloud Internet Services (CIS)** — WAF, DDoS, rate limiting, bot management on public apps
- **TLS 1.2+** minimum; HSTS on public endpoints

---

## 5. Compute and Kubernetes (IKS / ROKS)

### Virtual Server Instances (VSI)

- **Encrypted volumes** by default
- **SSH keys** in Secrets Manager; no password auth
- **Vulnerability Advisor** scan images and VSIs

### IBM Kubernetes Service (IKS)

- **Private service endpoint** for API server where possible
- **Image pull secrets** from container registry with IAM
- **Pod security standards** — restricted baseline
- **Calico network policies** default deny
- **Trusted Profile** mounted to worker nodes / pods for cloud API access
- **Key Protect** integration for etcd encryption at rest

### Code Engine / Cloud Functions

- **Trusted Profile** binding per app/function
- **Minimum instances** and concurrency limits for cost/abuse control

---

## 6. Data services

### Cloud Object Storage (COS)

- **IAM-only access**; disable public buckets (`firewall` + bucket policies)
- **Encryption**: SSE-KP with Key Protect/HPCS
- **Immutable retention** (Object Lock) for audit logs
- **Activity Tracker** data events for object read/write on sensitive buckets

### Databases (PostgreSQL, MongoDB, etc.)

- **Private endpoints** only
- **Encryption at rest** with customer-managed keys
- **Backup encryption**; test restore quarterly

---

## 7. Logging, monitoring, and compliance

| Service | Role |
|---------|------|
| Activity Tracker | All IAM and data plane events |
| Log Analysis | Query and dashboard |
| Monitoring | Metrics and alerts |
| Security and Compliance Center (SCC) | Posture management, CIS, ISO, PCI |

- **Activity Tracker** targets: COS bucket (immutable), Log Analysis, SIEM via Event Streams
- **SCC** — enable all relevant profiles; assign remediation owners
- **Vulnerability Advisor** + **Container Registry** image security

---

## 8. DevOps and supply chain

- **Toolchain** integrations use Trusted Profile / OIDC — no long-lived keys in pipeline env
- **Container Registry** — vulnerability scanning gate in deploy pipeline
- **Schematics/Terraform** state in COS with encryption and IAM lockdown

---

## 9. Agent / MCP on IBM Cloud

- Code Engine or IKS with **Trusted Profile** only
- Secrets from Secrets Manager at runtime
- Bastion MCP proxy; `bastion.yaml` rate limits and PII redaction
- Activity Tracker alert on anomalous secret read volume

---

## 10. Verification checklist

- [ ] MFA on all users
- [ ] Access groups (not ad-hoc user policies)
- [ ] No API keys for agent workloads
- [ ] Trusted Profile configured for compute
- [ ] HPCS/Key Protect for prod encryption keys
- [ ] COS buckets not public
- [ ] Activity Tracker to immutable COS
- [ ] SCC enabled with remediation SLA
- [ ] CIS WAF on public HTTP(S)

---

## 11. Red flags

- Service ID API key in Git or container env
- COS bucket with `allUsers` read
- Database with public service endpoint enabled
- Administrator role on service ID used by agent
- Activity Tracker not configured

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected (IBM Cloud / Bluemix):** see `cloud-well-architected-frameworks` — SCC profiles, Financial Services Framework, six pillars.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
