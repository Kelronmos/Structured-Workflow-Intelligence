"""Determinism suite for crypto audit."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_core.crypto_audit import (
    CryptoAuditError,
    compute_payload_hash,
    compute_state_hash,
    GENESIS_HASH,
    record_transition,
)


def test_same_payload_same_hash():
    p = {"b": 2, "a": 1}
    assert compute_payload_hash(p) == compute_payload_hash({"a": 1, "b": 2})


def test_key_order_independence():
    h1 = compute_payload_hash({"z": 1, "a": 2})
    h2 = compute_payload_hash({"a": 2, "z": 1})
    assert h1 == h2


def test_same_transition_same_state_hash():
    r1 = record_transition(
        workflow_id="W", transition_id="T", module_id="M", sequence_number=1, payload={"k": "v"}
    )
    r2 = record_transition(
        workflow_id="W", transition_id="T", module_id="M", sequence_number=1, payload={"k": "v"}
    )
    assert r1["state_hash"] == r2["state_hash"]


def test_different_payload_different_digest():
    assert compute_payload_hash({"n": 1}) != compute_payload_hash({"n": 2})


def test_different_module_different_state():
    h1 = compute_state_hash(module_id="A", previous_hash=GENESIS_HASH, payload_hash="c" * 64)
    h2 = compute_state_hash(module_id="B", previous_hash=GENESIS_HASH, payload_hash="c" * 64)
    assert h1 != h2


def test_different_previous_different_state():
    h1 = compute_state_hash(module_id="M", previous_hash="0" * 64, payload_hash="c" * 64)
    h2 = compute_state_hash(module_id="M", previous_hash="1" * 64, payload_hash="c" * 64)
    assert h1 != h2


def test_reject_float():
    try:
        compute_payload_hash({"x": 1.5})
        assert False
    except CryptoAuditError:
        pass


def test_reject_bytes():
    try:
        compute_payload_hash({"x": b"no"})
        assert False
    except CryptoAuditError:
        pass
