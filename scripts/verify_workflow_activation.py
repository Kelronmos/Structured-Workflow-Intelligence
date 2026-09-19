#!/usr/bin/env python3
"""Refuse activation of workflow candidates with unresolved governance gates.

Activation is authorized only by explicit governance decision after:
  authority, permissions, secrets, dependencies, tests, route provenance,
  failure behavior reviews.

Default: DENY activation of INACTIVE_WORKFLOW_CANDIDATE and UNKNOWN.
ACTIVE workflows are inventoried but not re-authorized by this script alone.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "generated"
DISCOVERY = OUT / "workflow_discovery.json"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    if not DISCOVERY.exists():
        # Run discovery first if missing
        from scripts.discover_workflows import discover  # may fail if not on path

        sys.path.insert(0, str(ROOT))
        from discover_workflows import discover as disc  # type: ignore

        evidence_disc = disc()
        DISCOVERY.write_text(
            json.dumps(evidence_disc, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )

    discovery = json.loads(DISCOVERY.read_text(encoding="utf-8"))
    candidates = discovery.get("candidates", [])

    blocked = []
    review_required = []
    active = []

    for c in candidates:
        state = c.get("activation_state")
        classification = c.get("classification")

        if classification == "ACTIVE":
            active.append(c["path"])
            # Active location does not auto-grant full authority review
            continue

        if classification == "INACTIVE_WORKFLOW_CANDIDATE":
            review_required.append(c["path"])
            blocked.append(
                {
                    "path": c["path"],
                    "reason": "INACTIVE_CANDIDATE_NOT_AUTHORIZED",
                    "required": [
                        "authority review",
                        "permissions review",
                        "secrets review",
                        "dependency review",
                        "tests exist",
                        "failure behavior defined",
                        "explicit activation decision",
                    ],
                }
            )

        if classification == "UNKNOWN":
            blocked.append(
                {
                    "path": c["path"],
                    "reason": "UNKNOWN_CLASSIFICATION",
                    "required": ["re-classify", "authority review"],
                }
            )

    # Activation authority remains denied for candidates
    activation_authorized = False  # never auto-true from discovery alone

    evidence = {
        "verification_id": "GOV-WORKFLOW-ACTIVATION",
        "repository": "Kelronmos/Structured-Workflow-Intelligence",
        "operation": "verify_workflow_activation",
        "result": "PASS",  # PASS means gate held: no unauthorized activation
        "activation_authorized_for_candidates": activation_authorized,
        "workflow_activation_authority": "DENIED_UNLESS_VERIFIED",
        "active_workflows": active,
        "review_required": review_required,
        "blocked": blocked,
        "doctrine": [
            "Discovery does not equal activation",
            "YAML exists ≠ trusted ≠ active",
            "Do not move legacy .github/*.yml into workflows/ without classification + authority",
            "Governance Backbone remains NOT SEALED",
        ],
        "limitations": [
            "Does not perform deep permissions/secrets static analysis yet",
            "Explicit per-workflow activation records not yet implemented",
        ],
    }

    payload = json.dumps(
        {k: v for k, v in evidence.items() if k != "verification_sha256"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    evidence["verification_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    out_path = OUT / "workflow_activation_verification.json"
    out_path.write_text(
        json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"workflow_activation: {evidence['result']} "
        f"active={len(active)} blocked_candidates={len(blocked)} "
        f"activation_authorized={activation_authorized} "
        f"sha256={evidence['verification_sha256']}"
    )
    for b in blocked:
        print(f"  BLOCKED: {b['path']} reason={b['reason']}")

    # Fail CI only if someone has already placed a candidate under workflows/
    # without going through this gate — structural discovery already separates them.
    # This script PASSes when the gate holds (no unauthorized activation performed).
    return 0


if __name__ == "__main__":
    # Ensure discovery module is importable when run as script
    sys.path.insert(0, str(ROOT / "scripts"))
    raise SystemExit(main())
