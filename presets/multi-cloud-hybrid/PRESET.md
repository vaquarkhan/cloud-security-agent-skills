---
preset_id: multi-cloud-hybrid
name: Multi-Cloud Hybrid Security
version: "1.0.0"
cloud_provider: multi
skills:
  - multi-cloud-security-posture
  - cloud-well-architected-frameworks
  - zero-trust-identity-and-secrets
  - using-cloud-security-agent-skills
---

# Multi-Cloud Hybrid Preset

For estates spanning AWS + Azure + GCP + OCI + IBM + Alibaba + Tanzu.

## Load order

1. `using-cloud-security-agent-skills`
2. `multi-cloud-security-posture`
3. `cloud-well-architected-frameworks`
4. Each in-scope **cloud skill**
5. `mcp-bastion-security-gateway`

## Unified baseline

Score all 12 domains in `multi-cloud-security-posture` before per-cloud depth.

## WAF matrix

`skills/cloud-well-architected-frameworks/references/well-architected-pillar-matrix.md`

## Demo

```bash
python examples/mock-posture-check/run_posture_check.py
```
