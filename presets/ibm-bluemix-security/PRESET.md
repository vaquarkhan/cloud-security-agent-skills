---
preset_id: ibm-bluemix-security
name: IBM Cloud Security (Bluemix legacy)
version: "1.0.0"
cloud_provider: ibm
legacy_names:
  - IBM Bluemix
  - Bluemix Cloud Foundry
frameworks:
  - IBM-Cloud-SCC
  - IBM-Financial-Services-Framework
skills:
  - ibm-cloud-security-best-practices
  - zero-trust-identity-and-secrets
---

# IBM Cloud / Bluemix Security Preset

**Bluemix** (2014–2019) is now **IBM Cloud**. Map legacy org/space → resource groups.

## Identity

- **Trusted Profile** only — `TRUSTED_PROFILE_NAME`
- Access groups (not ad-hoc user policies)

## Priority controls

| Area | Services |
|------|----------|
| IAM | IBMid, access groups, Trusted Profile |
| Encryption | Key Protect, HPCS |
| Detection | Activity Tracker, SCC |

## Bluemix migration

| Legacy | Current |
|--------|---------|
| Bluemix org/space | Resource groups |
| Bluemix API keys | Trusted Profile |
| CF on Bluemix | Tanzu or Code Engine |

## Checklist

`skills/ibm-cloud-security-best-practices/references/end-to-end-checklist.md`
