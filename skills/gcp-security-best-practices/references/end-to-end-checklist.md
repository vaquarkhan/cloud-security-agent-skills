# GCP End-to-End Security Checklist

Use with `gcp-security-best-practices` skill.

## Governance
- [ ] Organization + folders (prod/nonprod/sandbox)
- [ ] Org policies: disable SA key creation, require OS Login, domain restricted sharing
- [ ] VPC Service Controls perimeters for sensitive data
- [ ] Labels: environment, data_classification, owner

## IAM & Identity
- [ ] Google Workspace/Cloud Identity SSO; 2SV for admins
- [ ] No downloaded service account keys for workloads
- [ ] Workload Identity Federation for GKE/Cloud Run
- [ ] Custom roles where primitive roles too broad
- [ ] IAM Recommender reviewed quarterly

## Cloud KMS & Secrets
- [ ] CMEK for BigQuery, GCS, Cloud SQL, GKE secrets
- [ ] Secret Manager for app secrets; rotation
- [ ] KMS key rotation and IAM on key versions

## Network
- [ ] Shared VPC or isolated VPC per env
- [ ] Firewall rules default deny; hierarchical firewall policies
- [ ] Private Google Access; Private Service Connect
- [ ] Cloud Armor on external HTTPS load balancers
- [ ] VPC Flow Logs enabled

## Compute & GKE
- [ ] GKE private nodes + authorized networks
- [ ] Workload Identity on GKE service accounts
- [ ] Binary Authorization / image scanning
- [ ] Shielded GCE VMs

## Data
- [ ] GCS uniform bucket-level access; no public buckets
- [ ] Cloud SQL private IP; SSL required
- [ ] DLP on sensitive datasets

## Logging & Detection
- [ ] Admin Activity + Data Access audit logs exported
- [ ] Security Command Center Premium (if licensed)
- [ ] Log sinks to immutable GCS / BigQuery
- [ ] Alerts on IAM policy change, SA key create

## Compliance & Ops
- [ ] CIS GCP Benchmark via SCC
- [ ] Backup/DR for Cloud SQL and GKE state

## Agent / MCP
- [ ] Workload Identity for agent; no JSON keys
- [ ] Bastion proxy for MCP
