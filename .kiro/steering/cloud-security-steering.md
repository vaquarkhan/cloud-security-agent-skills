# Cloud Security Agent — Kiro steering

## Mission

Multi-cloud zero-trust security agent. No static credentials. MCP through Bastion only.

## Skill routing

| Signal | Skill |
|--------|-------|
| Session start | using-cloud-security-agent-skills |
| WAF review | cloud-well-architected-frameworks |
| AWS | aws-security-best-practices |
| Azure | azure-security-best-practices |
| GCP | gcp-security-best-practices |
| OCI | oci-oracle-cloud-security |
| IBM / Bluemix | ibm-cloud-security-best-practices |
| Alibaba | alibaba-cloud-security-best-practices |
| PCF / Tanzu | vmware-tanzu-pcf-security |
| Hybrid | multi-cloud-security-posture |

## Validation before PR

```bash
pytest tests/unit/
python scripts/validate-skills.py
python scripts/validate-assets.py
mcp-bastion validate --config bastion.yaml
```

## Forbidden

- Static API keys in code or config
- Direct MCP to agent.mcp_server without bastion_proxy
- Tool attribution footers in commits
