"""Route provenance tests — Policy 003 / Remediation-002 Tranche A."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.route_chain import (
    compute_route_hash,
    record_route,
    verify_route_record,
    verify_route_chain,
    reconstruct_route,
)
from admission.route_store import RouteStore, AppendOnlyViolation
from admission.route_canonical import canonicalize_route


def _origin():
    return {"repository": "Kelronmos/Structured-Workflow-Intelligence", "commit": "abc123"}


def test_canonical_is_deterministic():
    r1 = {
        "route_id": "R1",
        "operation_id": "OP1",
        "operation": "DISCOVER",
        "result": "ADMITTED",
        "origin": _origin(),
        "destination": {},
        "actor": "tester",
        "authority": "test",
        "purpose": None,
        "contract": {},
        "evidence": {},
        "parent_route_hash": None,
        "route": [],
    }
    # Different insertion order
    r2 = {
        "result": "ADMITTED",
        "route_id": "R1",
        "operation": "DISCOVER",
        "operation_id": "OP1",
        "origin": _origin(),
        "destination": {},
        "actor": "tester",
        "authority": "test",
        "purpose": None,
        "contract": {},
        "evidence": {},
        "parent_route_hash": None,
        "route": [],
    }
    assert canonicalize_route(r1) == canonicalize_route(r2)
    assert compute_route_hash(r1) == compute_route_hash(r2)


def test_record_and_verify():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        rec = record_route(
            route_id="R-001",
            operation_id="OP-001",
            operation="DISCOVER",
            result="ADMITTED",
            origin=_origin(),
            actor="ci",
            authority="governance",
            store=store,
        )
        assert rec["route_hash"]
        assert verify_route_record(rec)["ok"] is True
        loaded = store.read("R-001")
        assert loaded["route_hash"] == rec["route_hash"]


def test_append_only_violation():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        record_route(
            route_id="R-DUP",
            operation_id="OP",
            operation="PULL",
            result="ADMITTED",
            origin=_origin(),
            store=store,
        )
        try:
            record_route(
                route_id="R-DUP",
                operation_id="OP2",
                operation="PULL",
                result="ADMITTED",
                origin=_origin(),
                store=store,
            )
            assert False, "should have raised AppendOnlyViolation"
        except AppendOnlyViolation:
            pass


def test_chain_valid():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        r1 = record_route(
            route_id="C1",
            operation_id="O1",
            operation="DISCOVER",
            result="ADMITTED",
            origin=_origin(),
            parent_route_hash=None,
            store=store,
        )
        r2 = record_route(
            route_id="C2",
            operation_id="O2",
            operation="PULL",
            result="ADMITTED",
            origin=_origin(),
            parent_route_hash=r1["route_hash"],
            store=store,
        )
        r3 = record_route(
            route_id="C3",
            operation_id="O3",
            operation="EXECUTE",
            result="ADMITTED",
            origin=_origin(),
            parent_route_hash=r2["route_hash"],
            store=store,
        )
        chain = verify_route_chain([r1, r2, r3])
        assert chain["ok"] is True
        assert chain["length"] == 3


def test_chain_break_detected():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        r1 = record_route(
            route_id="B1",
            operation_id="O1",
            operation="DISCOVER",
            result="ADMITTED",
            origin=_origin(),
            store=store,
        )
        r2 = record_route(
            route_id="B2",
            operation_id="O2",
            operation="PULL",
            result="ADMITTED",
            origin=_origin(),
            parent_route_hash="deadbeef_wrong_parent",
            store=store,
        )
        result = verify_route_chain([r1, r2])
        assert result["ok"] is False
        assert result["reason"] == "CHAIN_BREAK"


def test_tamper_detected():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        r1 = record_route(
            route_id="T1",
            operation_id="O1",
            operation="INGEST",
            result="ADMITTED",
            origin=_origin(),
            store=store,
        )
        # Tamper after write
        r1["purpose"] = "tampered"
        result = verify_route_record(r1)
        assert result["ok"] is False
        assert result["reason"] == "ROUTE_HASH_MISMATCH"


def test_reconstruct():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        record_route(
            route_id="REC1",
            operation_id="O1",
            operation="BRIDGE",
            result="ADMITTED",
            origin=_origin(),
            destination={"repository": "Kelronmos/SWI-V2-Modules-11-22", "module": "M11"},
            store=store,
        )
        out = reconstruct_route("REC1", store=store)
        assert out["ok"] is True
        assert out["operation"] == "BRIDGE"
        assert out["destination"]["module"] == "M11"


def test_reconstruct_missing():
    with tempfile.TemporaryDirectory() as tmp:
        store = RouteStore(tmp)
        out = reconstruct_route("NO-SUCH", store=store)
        assert out["ok"] is False
        assert out["reason"] == "ROUTE_NOT_FOUND"


def test_invalid_result_rejected():
    try:
        canonicalize_route({
            "route_id": "X",
            "operation_id": "Y",
            "operation": "PULL",
            "result": "SUCCESS",  # invalid
            "origin": _origin(),
        })
        assert False, "should reject invalid result"
    except ValueError:
        pass
