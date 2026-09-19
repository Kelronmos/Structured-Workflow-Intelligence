"""SWI Cryptographic State Audit — SHA-256 hash chain (not Merkle).

Contract: docs/CRYPTOGRAPHIC_STATE_AUDIT_CONTRACT.md
component_id: SWI-CRYPTO-AUDIT
contract_version: 1.0-proposed
status: IMPLEMENTED_NOT_VERIFIED

Demonstrates integrity of recorded canonical representations and predecessor links.
Does NOT claim factual truth, storage immutability, non-repudiation, or authorization.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Iterable, List, Optional

GENESIS_HASH = "0" * 64
DOMAIN_PAYLOAD = "SWI-PAYLOAD-V1"
DOMAIN_STATE = "SWI-CRYPTO-AUDIT-STATE-V1"
RECEIPT_VERSION = 1

_SUPPORTED = (type(None), bool, int, str, list, dict)


class CryptoAuditError(ValueError):
    pass


def _reject_unsupported(obj: Any, path: str = "$") -> None:
    if isinstance(obj, float):
        raise CryptoAuditError(f"unsupported float at {path}")
    if type(obj) not in _SUPPORTED and not isinstance(obj, (list, dict)):
        # bool is subclass of int in Python — already allowed via bool check order
        if isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, str) or obj is None:
            return
        if isinstance(obj, list) or isinstance(obj, dict):
            pass
        else:
            raise CryptoAuditError(f"unsupported type {type(obj).__name__} at {path}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise CryptoAuditError(f"non-string key at {path}")
            _reject_unsupported(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _reject_unsupported(v, f"{path}[{i}]")


def canonical_serialize(data: Any) -> bytes:
    """Deterministic UTF-8 JSON bytes per contract."""
    _reject_unsupported(data)
    text = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return text.encode("utf-8")


def compute_payload_hash(payload: Any) -> str:
    body = {
        "domain": DOMAIN_PAYLOAD,
        "payload": payload,
    }
    return hashlib.sha256(canonical_serialize(body)).hexdigest()


def compute_state_hash(
    *,
    module_id: str,
    previous_hash: str,
    payload_hash: str,
) -> str:
    if not module_id:
        raise CryptoAuditError("empty module_id")
    if not previous_hash or len(previous_hash) != 64:
        raise CryptoAuditError("invalid previous_hash")
    if not payload_hash or len(payload_hash) != 64:
        raise CryptoAuditError("invalid payload_hash")
    body = {
        "domain": DOMAIN_STATE,
        "module_id": module_id,
        "previous_hash": previous_hash,
        "payload_hash": payload_hash,
    }
    return hashlib.sha256(canonical_serialize(body)).hexdigest()


def record_transition(
    *,
    workflow_id: str,
    transition_id: str,
    module_id: str,
    sequence_number: int,
    payload: Any,
    previous_hash: Optional[str] = None,
    recorded_at: Optional[str] = None,
) -> dict:
    if not workflow_id or not transition_id or not module_id:
        raise CryptoAuditError("workflow_id, transition_id, module_id required")
    if not isinstance(sequence_number, int) or sequence_number < 1:
        raise CryptoAuditError("sequence_number must be int >= 1")

    prev = previous_hash if previous_hash is not None else GENESIS_HASH
    payload_hash = compute_payload_hash(payload)
    state_hash = compute_state_hash(
        module_id=module_id,
        previous_hash=prev,
        payload_hash=payload_hash,
    )

    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "workflow_id": workflow_id,
        "transition_id": transition_id,
        "module_id": module_id,
        "sequence_number": sequence_number,
        "payload_hash": payload_hash,
        "previous_hash": prev,
        "state_hash": state_hash,
    }
    if recorded_at is not None:
        receipt["metadata"] = {"recorded_at": recorded_at}
    return receipt


def verify_receipt(
    receipt: dict,
    *,
    payload: Any,
    expected_previous_hash: Optional[str] = None,
) -> dict:
    """Independently recalculate payload and state hashes; compare."""
    required = [
        "receipt_version",
        "workflow_id",
        "transition_id",
        "module_id",
        "sequence_number",
        "payload_hash",
        "previous_hash",
        "state_hash",
    ]
    for k in required:
        if k not in receipt:
            return {"ok": False, "reason": "MISSING_FIELD", "field": k}

    if receipt["receipt_version"] != RECEIPT_VERSION:
        return {"ok": False, "reason": "UNSUPPORTED_RECEIPT_VERSION"}

    calc_payload = compute_payload_hash(payload)
    if not hmac.compare_digest(calc_payload, receipt["payload_hash"]):
        return {
            "ok": False,
            "reason": "PAYLOAD_HASH_MISMATCH",
            "expected": calc_payload,
            "observed": receipt["payload_hash"],
        }

    if expected_previous_hash is not None:
        if not hmac.compare_digest(expected_previous_hash, receipt["previous_hash"]):
            return {
                "ok": False,
                "reason": "PREVIOUS_HASH_MISMATCH",
                "expected": expected_previous_hash,
                "observed": receipt["previous_hash"],
            }

    calc_state = compute_state_hash(
        module_id=receipt["module_id"],
        previous_hash=receipt["previous_hash"],
        payload_hash=calc_payload,
    )
    if not hmac.compare_digest(calc_state, receipt["state_hash"]):
        return {
            "ok": False,
            "reason": "STATE_HASH_MISMATCH",
            "expected": calc_state,
            "observed": receipt["state_hash"],
        }

    return {"ok": True, "state_hash": calc_state, "payload_hash": calc_payload}


def verify_ledger(
    receipts: List[dict],
    payloads: List[Any],
) -> dict:
    if len(receipts) != len(payloads):
        return {"ok": False, "reason": "LENGTH_MISMATCH"}

    prev = GENESIS_HASH
    expected_seq = 1
    for i, (rec, payload) in enumerate(zip(receipts, payloads)):
        if rec.get("sequence_number") != expected_seq:
            return {
                "ok": False,
                "reason": "SEQUENCE_GAP",
                "index": i,
                "expected_sequence": expected_seq,
                "observed_sequence": rec.get("sequence_number"),
            }
        result = verify_receipt(rec, payload=payload, expected_previous_hash=prev)
        if not result.get("ok"):
            return {"ok": False, "index": i, "detail": result}
        prev = rec["state_hash"]
        expected_seq += 1

    return {"ok": True, "length": len(receipts), "final_state_hash": prev}
