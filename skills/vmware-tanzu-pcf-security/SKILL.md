---
name: vmware-tanzu-pcf-security
description: End-to-end VMware Tanzu / Cloud Foundry security — UAA/OAuth, CredHub, container hardening, network policies, Gorouter TLS, Loggregator, BOSH stemcells, TKG/Istio, and agent identity without static credentials.
---

# VMware Tanzu / Cloud Foundry (PCF) Security — End-to-End

## Overview

Security for **Tanzu Application Service (TAS/PCF)**, **Tanzu Kubernetes Grid (TKG)**, and **Tanzu Platform** deployments. Agents authenticate via **platform-issued credentials** (UAA client credentials grant, CredHub, or K8s service account tokens) — never static passwords in manifests or git.

---

## 1. Platform architecture and trust boundaries

### Foundations

- **Ops Manager** — admin access MFA, audit logging, locked-down network
- **BOSH Director** — credentials in CredHub; rotate regularly
- **Diego cells** — untrusted workload boundary; apps isolated via garden/guardian
- **Gorouter** — TLS termination, route integrity, rate limits
- **UAA** — central identity; OAuth2/OIDC for users and clients

### Separation

- **Org/Space** isolation for tenants; **Isolation Segments** for stronger network separation (NSX-T)
- **Prod / staging / dev** foundations or orgs separated
- **Shared services** org for platform tiles only — not tenant apps

---

## 2. Identity and access (UAA / SSO)

### Human users

- **Corporate IdP** (SAML/OIDC) federated to UAA — no local passwords for developers
- **MFA** at IdP for all platform users
- **Role assignment** — Org Manager, Space Developer, Space Auditor — least privilege
- **Break-glass** UAA admin — vaulted, monitored, quarterly test

### Application and agent clients

- **UAA client credentials** for service-to-service (agent → platform API)
- **Client secrets** stored in **CredHub** or **Vault** — injected at deploy via `cf set-env` / CredHub bindings, never in `manifest.yml` in git
- **Scopes** limited to required authorities (`cloud_controller.read`, custom scopes)
- **JWT validation** — apps verify issuer, audience, expiry; short-lived tokens

### TKG / Kubernetes path

- **OIDC** integration with UAA or corporate IdP for `kubectl`
- **RBAC** — namespace-scoped roles for developers; cluster-admin restricted
- **Service accounts** for agents with **TokenRequest** short-lived tokens
- **Workload identity** federation to cloud IAM where TKG runs on AWS/Azure/GCP (see respective cloud skills)

---

## 3. Secrets management (CredHub)

### CredHub

- **All platform secrets** — BOSH creds, tile passwords, service keys — in CredHub
- **Encryption** — CredHub encryption key in HSM or cloud KMS where supported
- **Rotation** — automate via BOSH CredHub rotation procedures
- **Access** — only BOSH/Ops Manager and authorized operators; audit all reads

### App secrets

- **User-provided services (UPS)** bind CredHub-backed credentials to apps
- **Spring Cloud / CredHub** integration for Java apps
- **Never** `cf set-env` with secrets in CI logs — use CredHub references or sealed secrets (TKG)

### TKG secrets

- **External Secrets Operator** → cloud KMS / Vault
- **Sealed Secrets** or **SOPS** for GitOps with encryption keys in KMS

---

## 4. Network security

### Cloud Foundry networking

- **Application Security Groups (ASGs)** — default deny egress; allowlist required FQDNs/IPs per space
- **Container-to-container networking** — disabled unless explicitly needed; **Network Policies** (CF Networking) default deny
- **Isolation Segments** — dedicated Diego cells + NSX-T segments for regulated workloads
- **Internal routes** — `*.apps.internal` not exposed via Gorouter; mTLS between internal services where supported

### Gorouter and TLS

- **TLS 1.2+** on all routes; **HSTS** for browser apps
- **Certificate management** — Ops Manager / Let's Encrypt / corporate PKI
- **Route services** for WAF (e.g., NSX Advanced Load Balancer, third-party)

### TKG networking

- **Antrea/Calico network policies** default deny
- **Istio service mesh** (optional) — mTLS STRICT mode, authorization policies
- **Ingress** — TLS at ingress controller; private ingress for internal APIs

---

## 5. Container and runtime hardening

### Diego / garden

- **Non-root** app users in buildpacks/containers where possible
- **Resource limits** — memory, disk, log rate
- **Staging droplets** scanned in pipeline (Clair, Trivy)
- **Rootfs** — latest stack (cflinuxfs4) patched via BOSH releases

### BOSH / stemcells

- **Regular stemcell updates** — critical CVE SLA (e.g., 14 days)
- **BOSH audit logs** exported to SIEM
- **Director** on private network; SSH via jump box only

### TKG clusters

- **Pod Security Standards** — restricted baseline minimum
- **Admission control** — OPA Gatekeeper / Kyverno deny privileged pods, hostPath, latest tag
- **Image pull** from trusted registry only; sign with Notation/Cosign

---

## 6. Data protection

### At rest

- **BOSH persistent disks** encrypted (IaaS volume encryption)
- **MySQL/Postgres tiles** — TDE where available; CredHub for credentials
- **Cloud blobstore** (S3/Azure/GCP) — SSE-KMS per cloud skill

### In transit

- **MySQL/Redis/RabbitMQ service tiles** — TLS bindings for apps
- **Diego cell ↔ Gorouter** — encrypted traffic
- **Loggregator** — TLS for log streams in modern TAS versions

---

## 7. Logging, monitoring, and audit

| Component | Purpose |
|-----------|---------|
| Loggregator / Firehose | App and platform logs |
| Cloud Foundry audit events | API actions (create app, bind service, scale) |
| Metrics (Healthwatch, Tanzu Observability) | Platform and app metrics |
| SIEM export | Nozzle / Log Insight / Splunk forwarder |
| Syslog drain | Per-app security event export |

- **Audit events** — retain per compliance; alert on `audit.app.create`, `audit.space.create`, admin login
- **App log redaction** — no secrets in stdout; Presidio/Bastion for agent MCP layer

---

## 8. Supply chain and deployment

- **Trusted builders** — only approved buildpacks and base images
- **Binary scanning** in CI before `cf push`
- **Ops Manager** — signed releases from VMware Tanzu Network; verify checksums
- **IaC** — Terraform for IaaS layer; secrets via Vault/CredHub not tfvars in git

---

## 9. Compliance and hardening benchmarks

- **CIS benchmarks** for underlying IaaS (AWS/Azure/vSphere) — see cloud-specific skills
- **DISA STIG** where required for government
- **PCI** — Isolation Segments, ASG egress lockdown, no shared tenancy on prod org

---

## 10. Agent / MCP on Tanzu

### Cloud Foundry deployment

- Deploy agent as **CF app** with **UAA client** from CredHub binding
- **ASG** allowlist only MCP Bastion endpoint and required cloud APIs
- **Route** internal-only if no public MCP needed
- **Zero Trust** — agent cloud calls use cloud-native identity (see AWS/Azure/GCP skills for IaaS layer)

### TKG deployment

- **Service account** + cloud workload identity for cloud API
- **NetworkPolicy** egress to Bastion proxy only
- **Secrets** via External Secrets Operator

---

## 11. Verification checklist

- [ ] UAA federated to corporate IdP with MFA
- [ ] No secrets in manifest.yml or git
- [ ] CredHub encryption key rotation scheduled
- [ ] ASGs default deny with documented exceptions
- [ ] Network policies enabled (CF Networking / TKG)
- [ ] TLS on all Gorouter routes
- [ ] Stemcell current within SLA
- [ ] Audit events exported to SIEM
- [ ] Isolation Segment for regulated apps (if required)
- [ ] Agent uses UAA client or K8s SA — no static cloud keys

---

## 12. Red flags

- `cf set-env` with production DB password in repo scripts
- ASG allowing `0.0.0.0/0` egress on prod spaces
- Org Manager role for all developers
- Public route to admin/Ops Manager UI
- Unpatched stemcell > 90 days behind current

---

## Reference checklist

Printable audit list: [references/end-to-end-checklist.md](references/end-to-end-checklist.md)

**Well-Architected (Pivotal PCF / Tanzu):** see `cloud-well-architected-frameworks` — NIST CSF + underlying IaaS WAF + six pillars.

## Related skills

- `cloud-well-architected-frameworks`
- `zero-trust-identity-and-secrets`
- `mcp-bastion-security-gateway`
- `aws-security-best-practices` / `azure-security-best-practices` / `gcp-security-best-practices` (IaaS under Tanzu)
- `multi-cloud-security-posture`
