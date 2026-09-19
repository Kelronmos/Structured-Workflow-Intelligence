"""Route hash-chain helpers (Policy 003 / Remediation §18).

Skeleton only. Append-only intent + verification shape.
Not yet a sealed production store.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, List


def _canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_route_hash(record: dict) -> str:
    payload = {k: v for k, v in record.items() if k != "route_hash"}
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def verify_route_record(record: dict) -> bool:
    if "route_hash" not in record:
        return False
    expected = record["route_hash"]
    actual = compute_route_hash(record)
    return expected == actual


def verify_route_chain(records: List[dict]) -> dict[str, Any]:
    """Verify sequential previous_route_hash linkage and individual hashes."""
    if not records:
        return {"ok": True, "length": 0}

    for i, rec in enumerate(records):
        if not verify_route_record(rec):
            return {
                "ok": False,
                "reason": "ROUTE_HASH_MISMATCH",
                "index": i,
                "route_id": rec.get("route_id"),
            }
        if i > 0:
            prev = records[i - 1]
            if rec.get("previous_route_hash") != prev.get("route_hash"):
                return {
                    "ok": False,
                    "reason": "CHAIN_BREAK",
                    "index": i,
                    "route_id": rec.get("route_id"),
                    "expected_previous": prev.get("route_hash"),
                    "observed_previous": rec.get("previous_route_hash"),
                }
    return {"ok": True, "length": len(records)}
