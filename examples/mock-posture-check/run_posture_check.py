#!/usr/bin/env python3
"""Run a multi-cloud security posture check on a mock (local) environment.

Demonstrates CloudSecurityAgent skill routing, Bastion config validation,
and posture assessment without requiring live cloud credentials.

Usage:
    python examples/mock-posture-check/run_posture_check.py
    python examples/mock-posture-check/run_posture_check.py --cloud aws
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.orchestrator import AgentConfig, CloudSecurityAgent  # noqa: E402


MOCK_CLOUDS = ("aws", "azure", "gcp", "oci", "ibm", "alibaba", "pcf")


def run_posture_check(clouds: list[str]) -> dict:
    agent = CloudSecurityAgent(AgentConfig(bastion_config=str(ROOT / "bastion.yaml")))
    posture = agent.validate_security_posture()
    results: dict = {
        "posture_summary": posture,
        "assessments": [],
    }

    for cloud in clouds:
        skill = agent.skills.load_for_cloud(cloud)
        bundle = skill.name if skill else "multi-cloud-security-posture"
        results["assessments"].append({
            "cloud": cloud,
            "primary_skill": bundle,
            "identity": "mock — no live credentials required",
            "checks": ["identity", "encryption", "network", "logging", "iam"],
            "status": "review_required",
            "preset": f"presets/{'tanzu-pcf' if cloud == 'pcf' else ('ibm-bluemix' if cloud == 'ibm' else cloud)}-security/PRESET.md",
        })

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Mock multi-cloud posture check")
    parser.add_argument(
        "--cloud",
        action="append",
        choices=MOCK_CLOUDS,
        help="Cloud to assess (repeatable; default: all)",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    clouds = args.cloud or list(MOCK_CLOUDS)

    results = run_posture_check(clouds)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("Cloud Security Agent — mock posture check\n")
        p = results["posture_summary"]
        print(f"  skills_complete: {p.get('skills_complete')}")
        print(f"  bastion_valid:   {p.get('bastion_valid')}")
        print(f"  available_count: {p.get('available_count')}\n")
        for a in results["assessments"]:
            print(f"  [{a['cloud'].upper()}] skill={a['primary_skill']} status={a['status']}")

    return 0 if results["posture_summary"].get("skills_complete") else 1


if __name__ == "__main__":
    raise SystemExit(main())
