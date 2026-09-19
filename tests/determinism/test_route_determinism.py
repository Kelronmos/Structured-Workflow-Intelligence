"""Determinism tests for route hashing (Remediation-002 Tranche B start)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.route_canonical import canonicalize_route
from admission.route_chain import compute_route_hash


def _record():
    return {
        "route_id": "D-001",
        "operation_id": "OP-D",
        "operation": "DISCOVER",
        "result": "ADMITTED",
        "origin": {"repository": "Kelronmos/Structured-Workflow-Intelligence", "commit": "cafebabe"},
        "destination": {"repository": "Kelronmos/SWI-V2-Modules-11-22", "module": "M11"},
        "actor": "determinism-test",
        "authority": "governance",
        "purpose": "determinism",
        "contract": {"id": "C1", "version": "1", "sha256": "ab"},
        "evidence": {"id": "E1", "sha256": "cd"},
        "parent_route_hash": None,
        "route": [],
    }


def test_identical_input_identical_hash():
    r = _record()
    h1 = compute_route_hash(r)
    h2 = compute_route_hash(r)
    h3 = compute_route_hash(dict(r))
    assert h1 == h2 == h3


def test_field_order_independence():
    a = _record()
    b = {
        "result": a["result"],
        "route_id": a["route_id"],
        "operation_id": a["operation_id"],
        "operation": a["operation"],
        "destination": a["destination"],
        "origin": a["origin"],
        "actor": a["actor"],
        "authority": a["authority"],
        "purpose": a["purpose"],
        "contract": a["contract"],
        "evidence": a["evidence"],
        "parent_route_hash": a["parent_route_hash"],
        "route": a["route"],
    }
    assert canonicalize_route(a) == canonicalize_route(b)
    assert compute_route_hash(a) == compute_route_hash(b)


def test_repeated_runs():
    r = _record()
    hashes = [compute_route_hash(r) for _ in range(5)]
    assert len(set(hashes)) == 1
