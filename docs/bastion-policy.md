# Bastion policy guide

How to review and tune `bastion.yaml` for enterprise compliance.

## Validate before deploy

```bash
mcp-bastion validate --config bastion.yaml
```

## Sections

| Section | Purpose | Production review |
|---------|---------|-------------------|
| `prompt_guard` | Meta PromptGuard injection defense | Ensure model deps installed |
| `pii` | Presidio entity redaction | Align `entities` with GDPR/HIPAA/PCI scope |
| `rate_limit` | Iteration cap, timeout, token budget | Set FinOps limits for your LLM spend |
| `circuit_breaker` | Disable failing tools after N errors | Keep enabled |
| `content_filter` | Block code paths, URLs, denylist regex | Add internal secret patterns |
| `rbac` | Tool permissions by role | Wire roles to your IdP |
| `cost_tracker` | Per-session and daily cost caps | Tune for budget |
| `audit` | Request audit log | Enable + ship to SIEM |
| `alerts` | Webhook on injection, rate limit, cost | Set `BASTION_WEBHOOK_URL` |

## PII entities (review with compliance)

Default entities in `bastion.yaml`:

- `US_SSN`, `US_PASSPORT`, `US_DRIVER_LICENSE`, `US_BANK_NUMBER`, `US_ITIN`
- `EMAIL_ADDRESS`, `PHONE_NUMBER`, `PERSON`, `LOCATION`
- `CREDIT_CARD`, `IBAN_CODE`, `MEDICAL_LICENSE`, `UK_NHS`, `IP_ADDRESS`

Adjust for your jurisdictions. Presidio uses `<ENTITY_TYPE>` replacement tokens unless `replacement_text` is set.

## Denylist patterns

Extend `content_filter.denylist_patterns` for org-specific secrets:

```yaml
denylist_patterns:
  - "(?i)password\\s*[:=]"
  - "(?i)api[_-]?key\\s*[:=]"
  - "(?i)your-internal-vault-uri-pattern"
```

## Rate limit and cycle detection

```yaml
rate_limit:
  enabled: true
  max_iterations: 15
  timeout_seconds: 120
  token_budget: 50000
  cycle_detection: true
  max_identical_calls: 5
```

Lower `max_iterations` and `token_budget` for cost-sensitive environments.

## Hot reload

```yaml
hot_reload:
  enabled: true
  poll_seconds: 2.0
```

Policy changes apply without restarting the MCP server when using `build_middleware_from_config()`.

## Related

- [MCP-Bastion POLICY_AS_CODE.md](https://github.com/vaquarkhan/MCP-Bastion/blob/main/docs/POLICY_AS_CODE.md)
- [architecture.md](architecture.md)
