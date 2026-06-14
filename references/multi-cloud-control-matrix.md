# Multi-cloud security control matrix (summary)

Quick reference — full WAF matrix in `skills/cloud-well-architected-frameworks/references/well-architected-pillar-matrix.md`.

| Control | AWS | Azure | GCP | OCI | IBM/Bluemix | Alibaba | PCF/Tanzu |
|---------|-----|-------|-----|-----|-------------|---------|-----------|
| Human SSO | IAM Identity Center | Entra ID | Cloud Identity | IDCS | IBMid | RAM federated | UAA SAML |
| Workload ID | IRSA / IAM role | Managed identity | Workload Identity | Resource principal | Trusted Profile | ECS RAM / RRSA | UAA / K8s SA |
| Secrets | Secrets Manager | Key Vault | Secret Manager | OCI Vault | Secrets Manager | Secrets Manager | CredHub |
| Keys | KMS | Key Vault keys | Cloud KMS | Vault keys | Key Protect/HPCS | KMS | CredHub + cloud KMS |
| Audit | CloudTrail | Activity Log | Audit Logs | Audit service | Activity Tracker | ActionTrail | CF audit events |
| CSPM | Security Hub | Defender | SCC | Cloud Guard | SCC | Security Center | IaaS layer |

Provenance: [registry/provenance.yaml](../registry/provenance.yaml)
