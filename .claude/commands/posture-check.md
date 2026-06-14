Run cloud security agent posture check and report skills completeness, Bastion validation, and primary cloud skill routing.

```bash
pip install -e .
cloud-security-agent
python scripts/validate-skills.py
python evals/benchmark/skill_routing_benchmark.py
```

Report: skills_complete, bastion_valid, available_count, any missing skills or benchmark failures.
