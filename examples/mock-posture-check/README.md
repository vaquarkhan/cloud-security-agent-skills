# Mock posture check example

Runnable demo — no cloud credentials required.

## Run

```bash
pip install -e .
python examples/mock-posture-check/run_posture_check.py
python examples/mock-posture-check/run_posture_check.py --cloud aws --cloud azure
python examples/mock-posture-check/run_posture_check.py --json
```

## What it demonstrates

- `CloudSecurityAgent.validate_security_posture()` — skills completeness, Bastion validation
- Per-cloud skill routing (`aws-security-best-practices`, etc.)
- Preset paths for each cloud

## Next steps

1. Load the matching preset under `presets/`
2. Run `mcp-bastion validate --config bastion.yaml`
3. Deploy agent with workload identity on your cloud (see cloud skill IAM sections)
