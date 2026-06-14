# Azure End-to-End Security Checklist

Use with `azure-security-best-practices` skill.

## Governance
- [ ] Management groups (Platform, Landing Zones, Sandbox)
- [ ] Azure Policy deny public storage, require TLS, require tags
- [ ] Subscription per environment; RBAC at MG scope
- [ ] Tags: Environment, DataClassification, Owner

## Entra ID & IAM
- [ ] Entra ID MFA for all users; CA policies block legacy auth
- [ ] PIM for privileged roles
- [ ] No client secrets on apps used by compute — managed identity
- [ ] RBAC least privilege; no Owner on prod subscriptions for devs
- [ ] Break-glass accounts monitored

## Key Vault & Encryption
- [ ] Key Vault per environment; purge protection + soft delete
- [ ] CMK for Storage, SQL, Cosmos, AKS etcd
- [ ] Secrets rotation in Key Vault
- [ ] Private endpoint for Key Vault

## Network
- [ ] Hub-spoke or VWAN topology
- [ ] NSGs default deny; Azure Firewall or NVA for egress
- [ ] Private endpoints for PaaS data plane
- [ ] DDoS Protection on public IPs (if applicable)
- [ ] WAF on Application Gateway / Front Door

## Compute & AKS
- [ ] AKS private cluster or authorized IP ranges
- [ ] Workload identity / managed identity for pods
- [ ] Defender for Containers enabled
- [ ] Disk encryption with CMK

## Data
- [ ] Storage account public access disabled
- [ ] SQL/Cosmos private endpoint only
- [ ] Purview classification on sensitive data stores

## Logging & Detection
- [ ] Activity Log to Log Analytics / Sentinel
- [ ] Diagnostic settings on all resources
- [ ] Microsoft Defender for Cloud plans enabled
- [ ] Sentinel analytics rules for identity anomalies

## Compliance & Ops
- [ ] Regulatory blueprint (PCI/HIPAA) if applicable
- [ ] Backup with encryption; restore tested

## Agent / MCP
- [ ] Managed identity for agent workload
- [ ] Bastion MCP proxy; AIV gate on PRs
