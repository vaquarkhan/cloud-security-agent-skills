# SME review and provenance

Reference checklists and WAF mappings include **provenance metadata** for audit evidence.

## Registry

[registry/provenance.yaml](../registry/provenance.yaml) tracks:

- Authoritative framework sources (CIS, AWS WAF, Azure WAF, GCP Architecture Framework, etc.)
- Review dates and owning skills
- Quarterly review policy

## Checklist footers

Each cloud checklist should include:

```markdown
> **Provenance:** CIS AWS Foundations v3.0 + AWS Well-Architected Security Pillar — reviewed YYYY-MM-DD.
> Source registry: registry/provenance.yaml
```

Example: [skills/aws-security-best-practices/references/end-to-end-checklist.md](../skills/aws-security-best-practices/references/end-to-end-checklist.md)

## CI enforcement

```bash
make validate-sme
python scripts/validate-skills.py
```

## Review cadence

| Activity | Frequency |
|----------|-----------|
| Framework version check | Quarterly |
| Checklist spot audit | Per major release |
| Provenance `last_updated` | Each release |

Update `registry/provenance.yaml` when CIS/WAF versions change.
