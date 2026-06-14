#!/usr/bin/env python3
"""Benchmark: agent skill routing and posture completeness.

Reproducible score for CI — measures whether core skills load and route correctly.
Run: python evals/benchmark/skill_routing_benchmark.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agent.skills_loader import CORE_SECURITY_SKILLS, SkillsLoader  # noqa: E402

EXPECTED_CLOUD_ROUTING = {
    "aws": "aws-security-best-practices",
    "azure": "azure-security-best-practices",
    "gcp": "gcp-security-best-practices",
    "oci": "oci-oracle-cloud-security",
    "ibm": "ibm-cloud-security-best-practices",
    "alibaba": "alibaba-cloud-security-best-practices",
    "pcf": "vmware-tanzu-pcf-security",
}


def run_benchmark() -> dict:
    loader = SkillsLoader()
    status = loader.status()
    scores: list[dict] = []
    passed = 0
    total = 0

    # Core registry completeness
    total += 1
    ok = status["skills_complete"] and status["available_count"] == len(CORE_SECURITY_SKILLS)
    if ok:
        passed += 1
    scores.append({"test": "core_skills_complete", "pass": ok, "detail": status})

    # Cloud routing
    for cloud, expected in EXPECTED_CLOUD_ROUTING.items():
        total += 1
        bundle = loader.load_for_cloud(cloud)
        ok = bundle is not None and bundle.name == expected
        if ok:
            passed += 1
        scores.append({"test": f"route_{cloud}", "pass": ok, "expected": expected, "got": bundle.name if bundle else None})

    # Meta skills have minimum body depth
    for name in ("cloud-well-architected-frameworks", "zero-trust-identity-and-secrets"):
        total += 1
        bundle = loader.load_skill(name)
        ok = bundle is not None and len(bundle.body.splitlines()) >= 100
        if ok:
            passed += 1
        scores.append({"test": f"depth_{name}", "pass": ok, "lines": len(bundle.body.splitlines()) if bundle else 0})

    pct = round(100 * passed / total) if total else 0
    return {
        "benchmark": "skill_routing_v1",
        "passed": passed,
        "total": total,
        "score_pct": pct,
        "results": scores,
    }


def main() -> int:
    report = run_benchmark()
    print(json.dumps(report, indent=2))
    print(f"\nScore: {report['score_pct']}% ({report['passed']}/{report['total']})")
    return 0 if report["score_pct"] == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
