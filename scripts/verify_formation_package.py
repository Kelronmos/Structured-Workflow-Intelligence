#!/usr/bin/env python3
"""Negative-control verification of FM-023–040 formation package.

Does NOT implement paths, seal modules, or authorize execution.
Exit 0 only if package remains PROPOSED / NOT_IMPLEMENTED under checks.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "docs/formation/fm_023_040_inventory.json"
SCHEMA_DIR = ROOT / "schemas/formation"
REPORT_PATH = ROOT / "docs/formation/NEGATIVE_CONTROL_VERIFICATION.md"

BOUND_COMMITS = (
    "ed7fb40a2b317096f0cdb79defe7234751972c0d",
    "1cf2eec1939aa878ee2c96ab3a154d73d8d3fb09",
)

errors: list[str] = []
passes: list[str] = []


def ok(msg: str) -> None:
    passes.append(msg)


def bad(msg: str) -> None:
    errors.append(msg)


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    if not INV.is_file():
        bad(f"missing inventory {INV}")
        return report()

    inv = load(INV)
    paths = inv.get("paths") or []
    if len(paths) == 18:
        ok("exactly 18 paths")
    else:
        bad(f"expected 18 paths, got {len(paths)}")

    for p in paths:
        pid = p.get("id", "?")
        if p.get("status") != "PROPOSED":
            bad(f"{pid}: status != PROPOSED ({p.get('status')})")
        if p.get("implementation_status") != "NOT_IMPLEMENTED":
            bad(f"{pid}: implementation_status != NOT_IMPLEMENTED")
        if p.get("proof_status") != "NONE":
            bad(f"{pid}: proof_status != NONE")
    if not any("status !=" in e or "implementation_status" in e or "proof_status" in e for e in errors):
        ok("every node PROPOSED / NOT_IMPLEMENTED / proof_status NONE")

    for key, val in [
        ("package_status", "PROPOSED"),
        ("implementation_status", "NOT_IMPLEMENTED"),
        ("proof_status", "NONE"),
    ]:
        if inv.get(key) != val:
            bad(f"inventory {key}={inv.get(key)!r} expected {val}")
        else:
            ok(f"inventory {key}={val}")

    for key in ("seal_status", "authorization_status", "execution_status"):
        v = inv.get(key)
        if v in (None, "NOT_APPLICABLE", "NOT_AUTHORIZED", "NOT_EXECUTABLE"):
            ok(f"inventory {key} non-promoting ({v})")
        else:
            bad(f"inventory {key} promotes: {v}")

    for name in [
        "swi-five-axis-separation.schema.json",
        "swi-formation-artifact.schema.json",
        "swi-formation-path-node.schema.json",
    ]:
        data = load(SCHEMA_DIR / name)
        enums: list = []

        def walk(o):
            if isinstance(o, dict):
                if isinstance(o.get("enum"), list):
                    enums.extend(o["enum"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for i in o:
                    walk(i)

        walk(data)
        if "ESTABLISHED" in enums or "SEALED" in enums:
            bad(f"{name}: enum contains ESTABLISHED or SEALED")
        else:
            ok(f"{name}: no ESTABLISHED/SEALED in enums")

    node_schema = load(SCHEMA_DIR / "swi-formation-path-node.schema.json")
    if node_schema.get("properties", {}).get("status", {}).get("const") == "PROPOSED":
        ok("path-node schema locks status to PROPOSED")
    else:
        bad("path-node schema does not lock status to PROPOSED")
    if (
        node_schema.get("properties", {}).get("implementation_status", {}).get("const")
        == "NOT_IMPLEMENTED"
    ):
        ok("path-node schema locks implementation_status to NOT_IMPLEMENTED")
    else:
        bad("path-node schema missing NOT_IMPLEMENTED lock")

    axes = {a["id"] for a in inv.get("five_axes") or []}
    if axes == {"A1", "A2", "A3", "A4", "A5"}:
        ok("five axes A1–A5 present")
    else:
        bad(f"axes incomplete: {axes}")

    example = load(SCHEMA_DIR / "examples/five_axis_posture.proposed.json")
    fi = example.get("forbidden_implications") or []
    pairs = {(x["from_axis"], x["to_axis"]) for x in fi}
    expected = {(a, b) for a in axes for b in axes if a != b}
    if pairs == expected and all(x.get("rule") == "MUST_NOT_INFER" for x in fi):
        ok("20 MUST_NOT_INFER pairs (no cross-axis inference)")
    else:
        bad(f"forbidden implications incomplete: {len(pairs)} pairs")

    if all(example["posture"][a]["state"] == "NOT_ASSESSED" for a in axes):
        ok("example posture all NOT_ASSESSED")
    else:
        bad("example posture not all NOT_ASSESSED")

    try:
        import jsonschema
    except ImportError:
        bad("jsonschema not installed")
        return report()

    sep_schema = load(SCHEMA_DIR / "swi-five-axis-separation.schema.json")
    art_schema = load(SCHEMA_DIR / "swi-formation-artifact.schema.json")

    good_sep = {
        "schema_version": "1.0.0",
        "package_status": "PROPOSED",
        "implementation_status": "NOT_IMPLEMENTED",
        "axes": {
            "A1": {"id": "A1", "name": "integrity"},
            "A2": {"id": "A2", "name": "truth"},
            "A3": {"id": "A3", "name": "authority"},
            "A4": {"id": "A4", "name": "path_closure"},
            "A5": {"id": "A5", "name": "legal_compliance"},
        },
        "posture": {a: {"state": "NOT_ASSESSED"} for a in "A1 A2 A3 A4 A5".split()},
        "forbidden_implications": [
            {"from_axis": a, "to_axis": b, "rule": "MUST_NOT_INFER"}
            for a in "A1 A2 A3 A4 A5".split()
            for b in "A1 A2 A3 A4 A5".split()
            if a != b
        ],
    }
    try:
        jsonschema.validate(good_sep, sep_schema)
        ok("valid five-axis document validates")
    except jsonschema.ValidationError as e:
        bad(f"valid five-axis should validate: {e.message}")

    for label, state in [("ESTABLISHED", "ESTABLISHED"), ("SEALED", "SEALED")]:
        t = json.loads(json.dumps(good_sep))
        t["posture"]["A1"]["state"] = state
        try:
            jsonschema.validate(t, sep_schema)
            bad(f"{label} posture was accepted (must reject)")
        except jsonschema.ValidationError:
            ok(f"{label} posture rejected by schema")

    bad_pkg = json.loads(json.dumps(good_sep))
    bad_pkg["package_status"] = "IMPLEMENTED"
    try:
        jsonschema.validate(bad_pkg, sep_schema)
        bad("package_status IMPLEMENTED accepted")
    except jsonschema.ValidationError:
        ok("package_status IMPLEMENTED rejected")

    good_node = {
        "id": "FM-023",
        "name": "Transaction Intake",
        "status": "PROPOSED",
        "implementation_status": "NOT_IMPLEMENTED",
        "proof_status": "NONE",
        "primary_axes": ["A1"],
        "depends_on": [],
    }
    jsonschema.validate(good_node, node_schema)
    ok("valid path node validates")

    for field, val, label in [
        ("status", "SEALED", "path node status SEALED"),
        ("implementation_status", "IMPLEMENTED", "path node IMPLEMENTED"),
    ]:
        t = dict(good_node)
        t[field] = val
        try:
            jsonschema.validate(t, node_schema)
            bad(f"{label} accepted")
        except jsonschema.ValidationError:
            ok(f"{label} rejected")

    art = {
        "schema_version": "1.0.0",
        "artifact_id": "x",
        "formation_path_id": "FM-023",
        "package_status": "PROPOSED",
        "implementation_status": "NOT_IMPLEMENTED",
        "axis_posture": {a: {"state": "NOT_ASSESSED"} for a in "A1 A2 A3 A4 A5".split()},
    }
    jsonschema.validate(art, art_schema)
    ok("formation artifact with full axis_posture validates")

    art_miss = dict(art)
    art_miss["axis_posture"] = {a: {"state": "NOT_ASSESSED"} for a in "A1 A2 A3 A4".split()}
    try:
        jsonschema.validate(art_miss, art_schema)
        bad("artifact missing A5 accepted")
    except jsonschema.ValidationError:
        ok("artifact missing A5 rejected")

    if inv.get("proof_status") == "NONE" and inv.get("package_status") == "PROPOSED":
        ok("package does not self-promote to proof/implementation")
    else:
        bad("package self-promotion detected")

    return report()


def report() -> int:
    lines = [
        "# Formation package — negative-control verification",
        "",
        "**Result package status (unchanged):** `PROPOSED` / `NOT_IMPLEMENTED`",
        "",
        "## Bound commits",
        "",
        "| SHA | Role |",
        "|-----|------|",
        f"| `{BOUND_COMMITS[0][:7]}` / full `{BOUND_COMMITS[0]}` | Machine inventory + schemas |",
        f"| `{BOUND_COMMITS[1][:7]}` / full `{BOUND_COMMITS[1]}` | Human map + five-axis example |",
        "",
        "This report challenges the documentation package; it does **not** implement FM-023–040,",
        "seal any module, authorize execution, or move paths into V1/V2.",
        "",
        "## Checks",
        "",
    ]
    for p in passes:
        lines.append(f"- [x] {p}")
    for e in errors:
        lines.append(f"- [ ] FAIL: {e}")
    lines += ["", "## Decision", ""]
    if errors:
        lines.append("**NEGATIVE CONTROL: FAILED**")
        code = 1
    else:
        lines.append("**NEGATIVE CONTROL: PASSED** — package remains non-promoting.")
        lines += [
            "",
            "```text",
            "PROPOSED / NOT_IMPLEMENTED",
            "proof_status: NONE",
            "No ESTABLISHED/SEALED posture enums accepted",
            "Cross-axis inference forbidden (MUST_NOT_INFER)",
            "FM-023–040 stay out of V1/V2 implementation surface",
            "```",
            "",
            "Re-run: `python3 scripts/verify_formation_package.py`",
        ]
        code = 0
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
