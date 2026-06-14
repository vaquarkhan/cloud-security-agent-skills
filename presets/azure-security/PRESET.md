---
preset_id: azure-security
name: Azure Security
version: "1.0.0"
cloud_provider: azure
frameworks:
  - Azure-Well-Architected
  - CIS-Azure-Foundations
skills:
  - azure-security-best-practices
  - zero-trust-identity-and-secrets
---

# Azure Security Preset

Entra ID, Key Vault, Defender, Sentinel — managed identity for agents.

## Identity

- Entra ID + CA + PIM for humans
- **User-assigned managed identity** for agents

## Priority controls

| Area | Services |
|------|----------|
| IAM | Entra ID, RBAC, PIM |
| Encryption | Key Vault, CMK |
| Network | Hub-spoke, Private Link, WAF |
| Detection | Defender for Cloud, Sentinel |

## Checklist

`skills/azure-security-best-practices/references/end-to-end-checklist.md`
