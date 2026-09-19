#!/usr/bin/env python3
"""Discover and classify .github workflow candidates.

Discovery does NOT equal activation.

States:
  ACTIVE                      — under .github/workflows/ (GitHub will run)
  INACTIVE_WORKFLOW_CANDIDATE — .yml under .github/ but not in workflows/
  NON_WORKFLOW_CONFIGURATION  — other config (FUNDING, JSON, etc.)
  UNKNOWN

Governance: workflow_activation_authority remains DENIED_UNLESS_VERIFIED
until independent review + activation authorization.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT / ".github"
WORKFLOWS = GITHUB / "workflows"
OUT = ROOT / "evidence" / "generated"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _parse_yaml_safe(path: Path) -> dict:
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return {"parses": True, "data": data if isinstance(data, dict) else {}}
    except Exception as e:
        return {"parses": False, "error": str(e), "data": {}}


def classify(path: Path) -> dict:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    entry = {
        "path": rel,
        "name": path.name,
        "size": path.stat().st_size,
        "sha256": _sha256_file(path),
        "classification": "UNKNOWN",
        "activation_state": "DISCOVERED",
        "yaml_parses": None,
        "has_on_trigger": None,
        "has_jobs": None,
        "name_field": None,
        "notes": [],
    }

    if path.suffix.lower() not in (".yml", ".yaml"):
        entry["classification"] = "NON_WORKFLOW_CONFIGURATION"
        entry["activation_state"] = "NOT_APPLICABLE"
        return entry

    parsed = _parse_yaml_safe(path)
    entry["yaml_parses"] = parsed["parses"]
    data = parsed.get("data") or {}

    if not parsed["parses"]:
        entry["classification"] = "UNKNOWN"
        entry["notes"].append("YAML does not parse")
        entry["activation_state"] = "REVIEW_REQUIRED"
        return entry

    entry["name_field"] = data.get("name")
    entry["has_on_trigger"] = "on" in data
    entry["has_jobs"] = "jobs" in data

    under_workflows = WORKFLOWS in path.parents or path.parent == WORKFLOWS

    if under_workflows and entry["has_on_trigger"] and entry["has_jobs"]:
        entry["classification"] = "ACTIVE"
        entry["activation_state"] = "ACTIVE"
        entry["notes"].append("Located under .github/workflows/ — GitHub Actions will execute")
    elif entry["has_on_trigger"] or entry["has_jobs"] or path.suffix in (".yml", ".yaml"):
        if under_workflows:
            entry["classification"] = "ACTIVE"
            entry["activation_state"] = "ACTIVE"
        else:
            entry["classification"] = "INACTIVE_WORKFLOW_CANDIDATE"
            entry["activation_state"] = "REVIEW_REQUIRED"
            entry["notes"].append(
                "Workflow-like YAML under .github/ but NOT under workflows/ — not auto-executed"
            )
    else:
        entry["classification"] = "NON_WORKFLOW_CONFIGURATION"
        entry["activation_state"] = "NOT_APPLICABLE"

    return entry


def discover() -> dict:
    if not GITHUB.is_dir():
        return {
            "result": "FAIL",
            "reason": "NO_GITHUB_DIR",
            "candidates": [],
        }

    candidates = []
    for path in sorted(GITHUB.rglob("*")):
        if path.is_file():
            candidates.append(classify(path))

    active = [c for c in candidates if c["classification"] == "ACTIVE"]
    inactive = [c for c in candidates if c["classification"] == "INACTIVE_WORKFLOW_CANDIDATE"]
    non_wf = [c for c in candidates if c["classification"] == "NON_WORKFLOW_CONFIGURATION"]
    unknown = [c for c in candidates if c["classification"] == "UNKNOWN"]

    evidence = {
        "verification_id": "GOV-WORKFLOW-DISCOVERY",
        "repository": "Kelronmos/Structured-Workflow-Intelligence",
        "operation": "discover_workflows",
        "result": "PASS",
        "summary": {
            "total": len(candidates),
            "active": len(active),
            "inactive_candidates": len(inactive),
            "non_workflow": len(non_wf),
            "unknown": len(unknown),
        },
        "candidates": candidates,
        "doctrine": [
            "Discovery does not equal activation",
            "YAML exists does not equal trusted",
            "workflow_activation_authority: DENIED_UNLESS_VERIFIED",
            "Governance Backbone remains NOT SEALED",
        ],
        "limitations": [
            "Classification is structural only",
            "Does not authorize secrets, deploy, or production workflows",
            "Permissions/secrets/authority review is separate",
        ],
    }

    payload = json.dumps(
        {k: v for k, v in evidence.items() if k != "verification_sha256"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    evidence["verification_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return evidence


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = discover()
    out_path = OUT / "workflow_discovery.json"
    out_path.write_text(
        json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    s = evidence["summary"]
    print(
        f"workflow_discovery: {evidence['result']} "
        f"active={s['active']} inactive_candidates={s['inactive_candidates']} "
        f"non_workflow={s['non_workflow']} unknown={s['unknown']} "
        f"sha256={evidence['verification_sha256']}"
    )
    for c in evidence["candidates"]:
        if c["classification"] in ("ACTIVE", "INACTIVE_WORKFLOW_CANDIDATE", "UNKNOWN"):
            print(f"  [{c['classification']}] {c['path']} state={c['activation_state']}")
    return 0 if evidence["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
