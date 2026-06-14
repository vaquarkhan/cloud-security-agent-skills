---
preset_id: tanzu-pcf-security
name: VMware Tanzu / Pivotal Cloud Foundry
version: "1.0.0"
cloud_provider: pcf
legacy_names:
  - Pivotal Cloud Foundry
  - PCF
  - PKS
skills:
  - vmware-tanzu-pcf-security
  - zero-trust-identity-and-secrets
---

# Tanzu / PCF Security Preset

**Pivotal Cloud Foundry (PCF)** → **VMware Tanzu Application Service (TAS)**.

## Identity

- UAA OAuth2 + **CredHub** — no secrets in `manifest.yml`

## Priority controls

| Area | Components |
|------|------------|
| Identity | UAA SAML, least-privilege org roles |
| Secrets | CredHub, UPS bindings |
| Network | ASGs default deny, isolation segments |
| Platform | Stemcell patching, audit events |

## Underlying IaaS

Apply AWS/Azure/GCP preset for foundation layer.

## Checklist

`skills/vmware-tanzu-pcf-security/references/end-to-end-checklist.md`
