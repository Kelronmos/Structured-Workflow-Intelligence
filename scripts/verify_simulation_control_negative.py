#!/usr/bin/env python3
"""Negative-control for Bidirectional Whole-Route Simulation package.

Bound to 77f4761c. PASS = resists semantic self-promotion; NOT simulator implemented.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUND_COMMIT = "77f4761cc81692ccdaf2173dfff7ea05e72a6505"
BOUND_SHORT = "77f4761c"

INV = ROOT / "docs/formation/fm_023_040_inventory.json"
CTRL = ROOT / "docs/formation/bidirectional_simulation_control.json"
FINDING_SCHEMA = ROOT / "schemas/formation/swi-simulation-finding.schema.json"
ROUTE_VERIFIED_SCHEMA = ROOT / "schemas/formation/swi-route-verified.schema.json"
DELTA_SCHEMA = ROOT / "schemas/formation/swi-route-delta.schema.json"
REPORT_JSON = ROOT / "docs/formation/SIMULATION_NEGATIVE_CONTROL_RESULT.json"
REPORT_MD = ROOT / "docs/formation/SIMULATION_NEGATIVE_CONTROL.md"

tests: dict[str, str] = {}
details: list[str] = []


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def mark(name: str, passed: bool, detail: str = "") -> None:
    tests[name] = "PASS" if passed else "FAIL"
    if detail:
        details.append(f"{name}: {detail}")


def must_reject(schema, instance, label: str) -> bool:
    import jsonschema

    try:
        jsonschema.validate(instance, schema)
        mark(label, False, "accepted promoting payload")
        return False
    except jsonschema.ValidationError:
        mark(label, True)
        return True


def must_accept(schema, instance, label: str) -> bool:
    import jsonschema

    try:
        jsonschema.validate(instance, schema)
        mark(label, True)
        return True
    except jsonschema.ValidationError as e:
        mark(label, False, e.message)
        return False


def base_finding():
    planes = {
        k: {"state": "NOT_ASSESSED"}
        for k in (
            "technical",
            "scar_risk",
            "human_ethical",
            "normative_legal",
            "institutional",
            "cross_jurisdictional",
        )
    }
    return {
        "schema_version": "1.0.0",
        "transition_id": "TR-NC-001",
        "from_path": "FM-029",
        "to_path": "FM-030",
        "package_status": "PROPOSED",
        "implementation_status": "NOT_IMPLEMENTED",
        "legal_status": "UNKNOWN",
        "applicability": "UNKNOWN",
        "evidence_basis": [],
        "conflicts": [],
        "uncertainties": ["negative_control"],
        "human_review_required": True,
        "execution_authorized": False,
        "common_sense": "UNKNOWN",
        "ethics_observation": "UNKNOWN",
        "scar_signal": "NONE",
        "planes": planes,
    }


def main() -> int:
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        print("FAIL: jsonschema required")
        return 1

    inv = load(INV)
    ctrl = load(CTRL)
    finding_schema = load(FINDING_SCHEMA)

    paths = inv.get("paths") or []
    mark(
        "fm_status_promotion",
        len(paths) == 18
        and all(p.get("status") == "PROPOSED" for p in paths)
        and all(p.get("implementation_status") == "NOT_IMPLEMENTED" for p in paths)
        and all(p.get("proof_status") == "NONE" for p in paths)
        and inv.get("package_status") == "PROPOSED"
        and inv.get("implementation_status") == "NOT_IMPLEMENTED"
        and inv.get("proof_status") == "NONE",
    )

    mark(
        "control_package_non_promoting",
        ctrl.get("package_status") == "PROPOSED"
        and ctrl.get("implementation_status") == "NOT_IMPLEMENTED"
        and ctrl.get("proof_status") == "NONE"
        and ctrl.get("execution_status") == "NOT_EXECUTABLE",
    )

    planes = set(ctrl.get("planes") or [])
    expected_planes = {
        "technical",
        "scar_risk",
        "human_ethical",
        "normative_legal",
        "institutional",
        "cross_jurisdictional",
    }
    mark("plane_collapse", planes == expected_planes)

    forbidden = set(ctrl.get("scar_meanings_forbidden") or [])
    mark(
        "scar_guilt_injection",
        "automatic_guilt" in forbidden and "automatic_illegality" in forbidden,
    )

    inv_ids = {i["id"] for i in ctrl.get("invariants") or []}
    mark(
        "unknown_promotion_invariants",
        {"I-SIM-002", "I-SIM-003"}.issubset(inv_ids),
    )

    good = base_finding()
    must_accept(finding_schema, good, "baseline_finding_valid")

    t = copy.deepcopy(good)
    t["execution_authorized"] = True
    must_reject(finding_schema, t, "execution_authorization_injection")

    for bad_val, label in [
        ("LEGAL", "legal_status_injection"),
        ("ILLEGAL", "illegal_status_injection"),
        ("CERTIFIED", "certification_injection"),
        ("APPROVED", "approval_injection"),
        ("SAFE", "safe_as_legal_status_injection"),
    ]:
        t = copy.deepcopy(good)
        t["legal_status"] = bad_val
        must_reject(finding_schema, t, label)

    for field in ("common_sense", "ethics_observation"):
        t = copy.deepcopy(good)
        t[field] = "LEGAL"
        must_reject(finding_schema, t, f"{field}_legal_injection")

    for bad in ("GUILTY", "ILLEGAL", "APPROVED"):
        t = copy.deepcopy(good)
        t["scar_signal"] = bad
        must_reject(finding_schema, t, f"scar_{bad.lower()}_injection")

    t = copy.deepcopy(good)
    del t["planes"]["cross_jurisdictional"]
    must_reject(finding_schema, t, "plane_missing_rejected")

    t = copy.deepcopy(good)
    t["legal_status"] = "AUTHORIZED"
    must_reject(finding_schema, t, "authority_as_legal_status_injection")

    t = copy.deepcopy(good)
    t["package_status"] = "IMPLEMENTED"
    must_reject(finding_schema, t, "package_status_promotion")

    t = copy.deepcopy(good)
    t["implementation_status"] = "IMPLEMENTED"
    must_reject(finding_schema, t, "implementation_status_promotion")

    if ROUTE_VERIFIED_SCHEMA.is_file():
        rv_schema = load(ROUTE_VERIFIED_SCHEMA)
        checks = {k: False for k in rv_schema["properties"]["checks"]["required"]}
        good_rv = {
            "schema_version": "1.0.0",
            "package_status": "PROPOSED",
            "implementation_status": "NOT_IMPLEMENTED",
            "route_verified": False,
            "execution_authorized": False,
            "checks": checks,
        }
        must_accept(rv_schema, good_rv, "route_verified_baseline")
        t = copy.deepcopy(good_rv)
        t["execution_authorized"] = True
        must_reject(rv_schema, t, "route_verified_execution_injection")
        t = copy.deepcopy(good_rv)
        t["route_verified"] = True
        t["execution_authorized"] = True
        must_reject(rv_schema, t, "simulation_success_cannot_authorize")

    if DELTA_SCHEMA.is_file():
        d_schema = load(DELTA_SCHEMA)
        good_d = {
            "schema_version": "1.0.0",
            "package_status": "PROPOSED",
            "implementation_status": "NOT_IMPLEMENTED",
            "transition_id": "TR-1",
            "from_state": "FM-023",
            "to_state": "FM-024",
            "state_before_hash": "a",
            "state_after_hash": "b",
            "execution_authorization_change": False,
        }
        must_accept(d_schema, good_d, "route_delta_baseline")
        t = copy.deepcopy(good_d)
        t["execution_authorization_change"] = True
        must_reject(d_schema, t, "route_delta_auth_change_injection")

    nc = " ".join(ctrl.get("non_claims") or [])
    inv_text = " ".join(i.get("statement", "") for i in ctrl.get("invariants") or [])
    blob = (nc + " " + inv_text).upper()
    mark(
        "axis_collapse",
        "EXECUTION" in blob
        and ("LEGAL" in blob or "I-SIM-002" in inv_ids)
        and ctrl.get("route_verified_implies_execution") is False,
    )
    mark(
        "unknown_promotion",
        "I-SIM-002" in inv_ids and tests.get("unknown_promotion_invariants") == "PASS",
    )
    mark("normative_requirement_applicability_separation", "I-SIM-006" in inv_ids)

    overall = "PASS" if all(v == "PASS" for v in tests.values()) else "FAIL"
    result = {
        "schema_version": "SIMULATION-NEGATIVE-CONTROL-1",
        "repository": "Structured-Workflow-Intelligence",
        "commit_sha": BOUND_COMMIT,
        "commit_sha_short": BOUND_SHORT,
        "package_status": "PROPOSED / NOT_IMPLEMENTED",
        "tests": tests,
        "overall": overall,
        "implementation_status": "NOT_IMPLEMENTED",
        "proof_status": "NONE",
        "interpretation": (
            "PASS means the proposed control package resists the tested forms of "
            "semantic self-promotion. It does NOT mean a simulator is implemented."
        ),
        "details": details,
    }
    REPORT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Simulation control — negative-control result",
        "",
        f"**Bound commit:** `{BOUND_SHORT}` (`{BOUND_COMMIT}`)",
        f"**Overall:** **{overall}**",
        "",
        "PASS means the design package resists semantic self-promotion.",
        "It does **not** mean the whole-route simulator is implemented.",
        "",
        "```text",
        "PROPOSED / NOT_IMPLEMENTED",
        "proof_status: NONE",
        "```",
        "",
        "Re-run: `python3 scripts/verify_simulation_control_negative.py`",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
