"""Minimal Route Recorder skeleton (Policy 003).

This is an implementation skeleton only.
It demonstrates append-only intent and hash chaining shape.
It is NOT yet a sealed, production-grade route provenance system.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional


def _canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_route_hash(record: dict) -> str:
    # Exclude route_hash itself from the hashed content
    payload = {k: v for k, v in record.items() if k != "route_hash"}
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def record_route(
    route_id: str,
    operation_id: str,
    origin: dict,
    result: str,
    *,
    actor: Optional[str] = None,
    authority: Optional[str] = None,
    route_nodes: Optional[list] = None,
    destination: Optional[dict] = None,
    purpose: Optional[str] = None,
    contract: Optional[dict] = None,
    evidence: Optional[dict] = None,
    parent_route: Optional[str] = None,
    previous_route_hash: Optional[str] = None,
    store_dir: str | Path = "evidence/routes",
) -> dict[str, Any]:
    """Create an append-only route record and persist it.

    Returns the full record including route_hash.
    """
    if result not in ("ADMITTED", "REJECTED", "HALTED"):
        raise ValueError("result must be ADMITTED | REJECTED | HALTED")

    record: dict[str, Any] = {
        "route_id": route_id,
        "operation_id": operation_id,
        "actor": actor,
        "authority": authority,
        "origin": origin or {},
        "route": route_nodes or [],
        "destination": destination or {},
        "purpose": purpose,
        "contract": contract or {},
        "result": result,
        "evidence": evidence or {},
        "parent_route": parent_route,
        "previous_route_hash": previous_route_hash,
    }
    record["route_hash"] = compute_route_hash(record)

    # Append-only persistence (simple file-per-record; later replace with proper store)
    root = Path(store_dir)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{route_id}.json"
    if path.exists():
        raise RuntimeError(f"Route record already exists (append-only violation): {path}")
    path.write_text(_canonical(record) + "\n", encoding="utf-8")

    return record
