"""Route provenance runtime — Policy 003 / SWI-GOV-REMEDIATION-002.

Implements:
- record_route
- compute_route_hash (canonical)
- verify_route_record
- verify_route_chain
- reconstruct_route

Fail-closed. Append-only. NOT SEALED.
"""

from __future__ import annotations

import hashlib
from typing import Any, List, Optional

from .route_canonical import canonicalize_route, ALLOWED_RESULTS
from .route_store import RouteStore, AppendOnlyViolation


def compute_route_hash(record: dict[str, Any]) -> str:
    canonical = canonicalize_route(record)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_route_record(record: dict[str, Any]) -> dict[str, Any]:
    if "route_hash" not in record:
        return {"ok": False, "reason": "MISSING_ROUTE_HASH"}
    expected = record["route_hash"]
    try:
        actual = compute_route_hash(record)
    except (TypeError, ValueError) as e:
        return {"ok": False, "reason": "CANONICALIZATION_FAILED", "detail": str(e)}
    if expected != actual:
        return {
            "ok": False,
            "reason": "ROUTE_HASH_MISMATCH",
            "expected": expected,
            "observed": actual,
        }
    return {"ok": True, "route_id": record.get("route_id"), "route_hash": expected}


def verify_route_chain(records: List[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {"ok": True, "length": 0}

    for i, rec in enumerate(records):
        vr = verify_route_record(rec)
        if not vr.get("ok"):
            return {
                "ok": False,
                "reason": vr.get("reason", "ROUTE_HASH_MISMATCH"),
                "index": i,
                "route_id": rec.get("route_id"),
                "detail": vr,
            }
        if i > 0:
            prev = records[i - 1]
            parent = rec.get("parent_route_hash")
            if parent != prev.get("route_hash"):
                return {
                    "ok": False,
                    "reason": "CHAIN_BREAK",
                    "index": i,
                    "route_id": rec.get("route_id"),
                    "expected_previous": prev.get("route_hash"),
                    "observed_previous": parent,
                }
    return {"ok": True, "length": len(records)}


def record_route(
    *,
    route_id: str,
    operation_id: str,
    operation: str,
    result: str,
    origin: dict,
    actor: Optional[str] = None,
    authority: Optional[str] = None,
    destination: Optional[dict] = None,
    purpose: Optional[str] = None,
    contract: Optional[dict] = None,
    evidence: Optional[dict] = None,
    route_nodes: Optional[list] = None,
    parent_route_hash: Optional[str] = None,
    store: Optional[RouteStore] = None,
) -> dict[str, Any]:
    """Create, hash, and append-only persist a route record."""
    if result not in ALLOWED_RESULTS:
        raise ValueError(f"invalid result: {result}")

    record: dict[str, Any] = {
        "route_id": route_id,
        "operation_id": operation_id,
        "actor": actor,
        "authority": authority,
        "operation": operation,
        "origin": origin or {},
        "destination": destination or {},
        "purpose": purpose,
        "contract": contract or {},
        "result": result,
        "evidence": evidence or {},
        "parent_route_hash": parent_route_hash,
        "route": route_nodes or [],
    }
    record["route_hash"] = compute_route_hash(record)

    store = store or RouteStore()
    try:
        store.write(route_id, record)
    except AppendOnlyViolation:
        raise

    return record


def reconstruct_route(
    route_id: str,
    store: Optional[RouteStore] = None,
) -> dict[str, Any]:
    """Load a route and verify its hash. Returns the record or failure."""
    store = store or RouteStore()
    try:
        record = store.read(route_id)
    except FileNotFoundError:
        return {"ok": False, "reason": "ROUTE_NOT_FOUND", "route_id": route_id}

    vr = verify_route_record(record)
    if not vr.get("ok"):
        return {"ok": False, "reason": "ROUTE_INTEGRITY_FAILED", "detail": vr, "route_id": route_id}

    return {
        "ok": True,
        "route_id": route_id,
        "origin": record.get("origin"),
        "destination": record.get("destination"),
        "operation": record.get("operation"),
        "result": record.get("result"),
        "evidence": record.get("evidence"),
        "route": record.get("route"),
        "route_hash": record.get("route_hash"),
        "parent_route_hash": record.get("parent_route_hash"),
        "record": record,
    }
