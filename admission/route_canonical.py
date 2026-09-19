"""Canonical route serialization (SWI-GOV-REMEDIATION-002 §7).

Deterministic field ordering, stable JSON, no nondeterministic values.
Hash is always computed from the canonical representation.
"""

from __future__ import annotations

import json
from typing import Any


ALLOWED_RESULTS = frozenset({"ADMITTED", "REJECTED", "HALTED"})

# Fields included in canonical form (order is fixed for stability)
CANONICAL_KEYS = (
    "route_id",
    "operation_id",
    "actor",
    "authority",
    "operation",
    "origin",
    "destination",
    "purpose",
    "contract",
    "result",
    "evidence",
    "parent_route_hash",
    "route",
)


def _reject_nondeterministic(obj: Any, path: str = "") -> None:
    if isinstance(obj, float):
        raise ValueError(f"Float values are not allowed in route records (path={path})")
    if isinstance(obj, dict):
        for k, v in obj.items():
            _reject_nondeterministic(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _reject_nondeterministic(v, f"{path}[{i}]")


def canonicalize_route(record: dict[str, Any]) -> str:
    """Return deterministic canonical JSON (UTF-8 string) excluding route_hash."""
    if not isinstance(record, dict):
        raise TypeError("route record must be a dict")

    result = record.get("result")
    if result not in ALLOWED_RESULTS:
        raise ValueError(f"invalid result: {result!r}; allowed={sorted(ALLOWED_RESULTS)}")

    # Build ordered payload; omit route_hash from hashed content
    payload: dict[str, Any] = {}
    for key in CANONICAL_KEYS:
        if key in record:
            payload[key] = record[key]

    # Include any extra governed keys in sorted order (except route_hash)
    extras = sorted(k for k in record.keys() if k not in CANONICAL_KEYS and k != "route_hash")
    for key in extras:
        payload[key] = record[key]

    _reject_nondeterministic(payload)

    return json.dumps(payload, sort_keys=False, separators=(",", ":"), ensure_ascii=True)
