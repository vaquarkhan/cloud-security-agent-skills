---
preset_id: gcp-security
name: GCP Security
version: "1.0.0"
cloud_provider: gcp
frameworks:
  - Google-Cloud-Architecture-Framework
  - CIS-GCP-Foundations
skills:
  - gcp-security-best-practices
  - zero-trust-identity-and-secrets
---

# GCP Security Preset

Org policies, Workload Identity, Cloud KMS/CMEK, Security Command Center.

## Identity

- Workload Identity Federation — **no downloaded SA JSON keys**

## Priority controls

| Area | Services |
|------|----------|
| Governance | Org policies, VPC Service Controls |
| IAM | Workload Identity, custom roles |
| Encryption | Cloud KMS, Secret Manager |
| Detection | SCC, audit log exports |

## Checklist

`skills/gcp-security-best-practices/references/end-to-end-checklist.md`
