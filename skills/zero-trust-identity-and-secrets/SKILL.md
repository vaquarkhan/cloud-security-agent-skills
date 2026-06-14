---
name: zero-trust-identity-and-secrets
description: End-to-end zero-trust identity — no static API keys, short-lived credentials, IdentityManager for AWS/Azure/GCP/OCI/IBM/Alibaba/PCF, secret lifecycle, MCP Bastion redaction, and verification across all clouds.
---

# Zero-Trust Identity and Secrets (End-to-End)

## Overview

Zero-trust for cloud security agents means **never trust, always verify** — every request authenticated, authorized, encrypted, and logged. **No static secrets** in source, git, CI variables, container images, or MCP tool arguments.

Applies to **all clouds** in this repo. Pair with the matching cloud skill for service-specific IAM/KMS/vault controls.

---

## 1. Core principles

| Principle | Implementation |
|-----------|----------------|
| No long-lived keys | Roles, managed identity, workload identity, STS, resource principals |
| Least privilege | One identity per workload; scope to resource ARN/key/vault secret |
| Short sessions | Max session duration 1h (often 15m) for sensitive roles |
| Encrypt everywhere | TLS 1.2+ in transit; CMK/HSM at rest |
| Assume breach | Logging, alerting, blast-radius limits, no silent fail-open |
| Verify continuously | Access Analyzer, SCC, Security Hub, periodic access reviews |

---

## 2. IdentityManager mapping (this repo)

| Cloud | Class | Mechanism | Env / platform |
|-------|-------|-----------|----------------|
| AWS | `AWSCredentialChainManager` | IAM role chain, IRSA, instance profile | Pod SA annotation, EC2 profile |
| Azure | `AzureDefaultCredentialManager` | Managed identity, workload identity | `AZURE_CLIENT_ID`, federated cred |
| GCP | `GCPDefaultCredentialManager` | ADC, workload identity | GSA ↔ K8s SA binding |
| OCI | `OCIResourcePrincipalManager` | Resource / instance principal | `OCI_RESOURCE_PRINCIPAL_*` |
| IBM | `IBMTrustedProfileManager` | Trusted Profile only | `TRUSTED_PROFILE_NAME` |
| Alibaba | `AlibabaRAMRoleManager` | ECS RAM role, RRSA | Instance metadata STS |
| PCF | `PCFCredHubManager` | UAA OAuth2, CredHub bindings | `VCAP_SERVICES`, CredHub |

### Code pattern

```python
from security import get_identity_manager

manager = get_identity_manager()  # auto-detects runtime cloud
creds = manager.refresh_if_needed()
# Use creds with cloud SDK — never hard-code keys
```

### Introspection

`security/introspection.py` detects runtime environment (metadata service, env hints). **Always introspect** before assuming a cloud.

---

## 3. Forbidden patterns (reject in review and AIV)

### Never in application code or committed config

- `aws_access_key_id` / `AWS_SECRET_ACCESS_KEY`
- `client_secret=` / `AZURE_CLIENT_SECRET` (for workloads — use MI)
- GCP JSON service account key files in repo
- OCI API signing key PEM in repo
- IBM Cloud API key on service ID used by compute
- Alibaba `AccessKeyId` / `AccessKeySecret`
- PCF passwords or UAA client secrets in `manifest.yml` / git
- `Bearer eyJ...` long-lived JWTs in source
- `password=`, `api_key=`, `token=` literals in Python/ YAML/ Terraform **values** (use vault references)

### Never in MCP layer

- Raw `agent.mcp_server` without `agent.bastion_proxy`
- Tool handlers returning unredacted secrets from env
- Passing user-supplied credentials through to cloud APIs without validation

---

## 4. Secret lifecycle (all clouds)

### Creation

- Generate in **vault service** (Secrets Manager, Key Vault, Secret Manager, OCI Vault, IBM Secrets Manager, Alibaba Secrets Manager, CredHub)
- **Never** generate in chat, ticket, or email

### Storage

- Vault with **CMK/HSM** encryption
- **RBAC** scoped to secret ARN/name
- **Audit** every read (`GetSecretValue`, etc.)

### Rotation

- **Automated rotation** where supported (90d default for DB passwords)
- **Dual-write** period during rotation for apps
- **Break-glass** secrets: rotate immediately after use

### Disposal

- Revoke old versions after rotation
- **Git history** — if secret ever committed: rotate + purge history or treat as compromised

---

## 5. Human vs workload identity

### Humans

- Federated SSO (IAM Identity Center, Entra ID, Google Workspace, OCI IDCS, IBMid, RAM federated, UAA SAML)
- **MFA mandatory** — hardware key for admins
- **PIM / just-in-time** admin where available
- **No shared accounts**

### Workloads / agents

- **Platform-assigned identity only**
- CI/CD: **OIDC federation** to cloud (GitHub Actions, GitLab, Azure DevOps) — no pipeline secrets
- **Permission boundaries** (AWS) / equivalent scoping on all creatable roles

---

## 6. Network zero-trust (identity complement)

- **Private endpoints** for vault, object storage, databases
- **Default deny** security groups / NSGs / firewall rules
- **mTLS** service-to-service where supported
- Agent egress **allowlist** only (MCP Bastion + required cloud API endpoints)

---

## 7. MCP and LLM boundary

- **Bastion proxy** mandatory — `bastion.yaml`:
  - **Presidio** redacts PII before LLM context
  - **Content filter** blocks API key patterns in tool output
  - **PromptGuard** blocks injection in tool arguments
- Agents must **not** echo cloud credentials in tool responses
- Log Bastion audit trail; alert on filter triggers

---

## 8. Per-cloud identity quick reference

### AWS
- IAM Identity Center for humans; IRSA/instance profile for agents
- Deny `iam:CreateAccessKey` via SCP except break-glass

### Azure
- Entra ID + CA policies; user-assigned MI for agents
- No client secrets on App Registrations used by compute

### GCP
- Org constraints: `iam.disableServiceAccountKeyCreation`
- Workload Identity Federation for GKE/Cloud Run agents

### OCI
- Dynamic groups + resource principal; API keys eliminated for workloads

### IBM
- Trusted Profile on Code Engine/IKS; access groups not user policies

### Alibaba
- ECS RAM role / RRSA; control policy deny AccessKey creation

### PCF / Tanzu
- UAA client credentials from CredHub; K8s SA tokens on TKG

---

## 9. Verification checklist

- [ ] `get_identity_manager()` used — no manual key construction
- [ ] No secret literals in git diff (`git secrets` / AIV design rules)
- [ ] Credentials auto-refresh (STS/session expiry handled)
- [ ] Vault RBAC least privilege on every secret/key
- [ ] MCP client uses `agent.bastion_proxy`
- [ ] Cloud audit logging enabled for identity API calls
- [ ] Quarterly access review scheduled
- [ ] Break-glass procedure documented and tested

---

## 10. Red flags

- "Temporary" access key still active after 90 days
- Agent role with `*` admin on data plane
- Secret in environment variable in Dockerfile
- Developer pastes cloud creds into Cursor chat (rotate immediately)
- Bastion disabled "for debugging"

---

## Related skills

- Cloud-specific: `aws-security-best-practices`, `azure-security-best-practices`, etc.
- `mcp-bastion-security-gateway`
- `multi-cloud-security-posture`
- `pr-integrity-aiv-gate`
