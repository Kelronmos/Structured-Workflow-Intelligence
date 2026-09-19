"""HALT Controller — SWI-POLICY-001 / FAILURE_POLICY

Never silently return False.
Always generate machine-readable evidence + deterministic hash.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional


def _canonical_json(obj: dict) -> str:
    """Deterministic serialization (sorted keys, no whitespace variance)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def halt(
    module: str,
    reason: str,
    required: str,
    observed: str,
    dependency: Optional[str] = None,
    commit: Optional[str] = None,
    contract_sha256: Optional[str] = None,
    extra: Optional[dict] = None,
) -> dict[str, Any]:
    """Generate a HALT evidence event.

    Returns the event dict. Caller is responsible for persistence
    if the full evidence pipeline is active.
    """
    event: dict[str, Any] = {
        "event": "ADMISSION_HALTED",
        "module": module,
        "reason": reason,
        "required": required,
        "observed": observed,
        "dependency": dependency,
        "commit": commit,
        "contract_sha256": contract_sha256,
        "action": "HALT",
    }
    if extra:
        event.update(extra)

    canonical = _canonical_json(event)
    event_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    event["event_sha256"] = event_hash

    return event


def persist_halt(event: dict[str, Any], evidence_root: str | Path = "evidence") -> Path:
    """Write JSON + SHA-256 + human report under evidence/."""
    root = Path(evidence_root)
    json_dir = root / "json"
    hash_dir = root / "hashes"
    report_dir = root / "reports"
    for d in (json_dir, hash_dir, report_dir):
        d.mkdir(parents=True, exist_ok=True)

    event_id = event.get("event_sha256", "unknown")[:16]
    json_path = json_dir / f"{event_id}.json"
    hash_path = hash_dir / f"{event_id}.sha256"
    report_path = report_dir / f"{event_id}.txt"

    canonical = _canonical_json(event)
    json_path.write_text(canonical + "\n", encoding="utf-8")
    hash_path.write_text(event["event_sha256"] + "\n", encoding="utf-8")

    report = (
        f"ADMISSION HALTED\n"
        f"================\n"
        f"Module     : {event.get('module')}\n"
        f"Reason     : {event.get('reason')}\n"
        f"Required   : {event.get('required')}\n"
        f"Observed   : {event.get('observed')}\n"
        f"Dependency : {event.get('dependency')}\n"
        f"Commit     : {event.get('commit')}\n"
        f"Contract   : {event.get('contract_sha256')}\n"
        f"SHA-256    : {event.get('event_sha256')}\n"
        f"Action     : HALT — NO EXECUTION\n"
    )
    report_path.write_text(report, encoding="utf-8")
    return json_path
