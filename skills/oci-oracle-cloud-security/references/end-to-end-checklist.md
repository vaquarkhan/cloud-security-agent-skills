# OCI End-to-End Security Checklist

Use with `oci-oracle-cloud-security` skill.

## Governance
- [ ] Compartment hierarchy (Security, Network, Workloads)
- [ ] Tag defaults on compartments
- [ ] Security Zone on prod compartment
- [ ] Federated IdP; no daily local users

## IAM
- [ ] MFA for all users
- [ ] Policies on groups; least privilege statements
- [ ] Dynamic groups for compute/functions
- [ ] Resource principal for agents — no API signing keys
- [ ] Break-glass local admin vaulted and monitored

## Vault & Encryption
- [ ] HSM vault for prod keys
- [ ] Object Storage SSE with Vault key
- [ ] Block/database encryption with Vault CMK
- [ ] Secret rotation schedule

## Network
- [ ] VCN hub-spoke; private subnets for apps/DB
- [ ] NSGs default deny; VCN Flow Logs all subnets
- [ ] Service Gateway + NAT; no public DB IPs
- [ ] OCI WAF on public load balancers

## Compute & OKE
- [ ] OKE private API endpoint
- [ ] Resource principal for pod workloads
- [ ] Bastion service for SSH (no public SSH)

## Data
- [ ] No public Object Storage buckets
- [ ] ADB/DBCS private endpoint; Data Safe enabled

## Logging & Detection
- [ ] Audit service export to immutable bucket
- [ ] Cloud Guard targets all compartments
- [ ] Log Analytics + Service Connector Hub to SIEM
- [ ] Alerts on policy/vault/API key events

## Agent / MCP
- [ ] Resource principal + optional Vault
- [ ] Bastion MCP proxy
