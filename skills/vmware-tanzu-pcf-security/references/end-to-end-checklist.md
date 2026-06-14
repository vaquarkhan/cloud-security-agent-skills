# VMware Tanzu / PCF End-to-End Security Checklist

Use with `vmware-tanzu-pcf-security` skill.

## Platform governance
- [ ] Separate foundations/orgs for prod vs nonprod
- [ ] Ops Manager access MFA + audit
- [ ] Isolation Segments for regulated workloads (if required)

## UAA & Identity
- [ ] Corporate IdP federated to UAA; MFA at IdP
- [ ] Least privilege org/space roles
- [ ] UAA client credentials from CredHub — not git
- [ ] TKG OIDC for kubectl; RBAC namespace-scoped

## CredHub & Secrets
- [ ] All platform secrets in CredHub
- [ ] CredHub encryption key rotation scheduled
- [ ] App secrets via UPS/CredHub bindings or External Secrets (TKG)

## Network
- [ ] ASGs default deny egress with documented allowlist
- [ ] CF Networking policies default deny (if enabled)
- [ ] TLS on all Gorouter routes; HSTS
- [ ] TKG NetworkPolicy / Istio STRICT mTLS (if mesh)

## Runtime hardening
- [ ] Current stemcell within patch SLA
- [ ] Non-root app users where possible
- [ ] Image/droplet scan in CI
- [ ] TKG Pod Security Standards restricted

## Logging & Audit
- [ ] CF audit events to SIEM
- [ ] Loggregator drains for security apps
- [ ] BOSH audit logs retained

## Underlying IaaS
- [ ] Apply AWS/Azure/GCP skill for foundation IaaS layer

## Agent / MCP
- [ ] UAA client or K8s SA — no static cloud keys
- [ ] ASG egress to Bastion only
- [ ] Bastion proxy for MCP
