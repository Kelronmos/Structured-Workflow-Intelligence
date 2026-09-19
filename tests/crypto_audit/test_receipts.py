"""Crypto audit positive + basic chain tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_core.crypto_audit import (
    GENESIS_HASH,
    compute_payload_hash,
    record_transition,
    verify_ledger,
    verify_receipt,
)


def test_single_transition_verifies():
    payload = {"amount": 500, "currency": "BWP"}
    r = record_transition(
        workflow_id="WF-TEST",
        transition_id="T1",
        module_id="MODULE_01",
        sequence_number=1,
        payload=payload,
        previous_hash=GENESIS_HASH,
        recorded_at="2026-09-19T18:00:00Z",  # metadata only
    )
    assert r["previous_hash"] == GENESIS_HASH
    assert verify_receipt(r, payload=payload, expected_previous_hash=GENESIS_HASH)["ok"]


def test_timestamp_does_not_affect_state_hash():
    payload = {"x": 1}
    r1 = record_transition(
        workflow_id="WF",
        transition_id="T1",
        module_id="M",
        sequence_number=1,
        payload=payload,
        recorded_at="2020-01-01T00:00:00Z",
    )
    r2 = record_transition(
        workflow_id="WF",
        transition_id="T1",
        module_id="M",
        sequence_number=1,
        payload=payload,
        recorded_at="2099-12-31T23:59:59Z",
    )
    assert r1["state_hash"] == r2["state_hash"]
    assert r1["payload_hash"] == r2["payload_hash"]


def test_chain_of_three():
    payloads = [{"n": 1}, {"n": 2}, {"n": 3}]
    receipts = []
    prev = GENESIS_HASH
    for i, p in enumerate(payloads, start=1):
        r = record_transition(
            workflow_id="WF-CHAIN",
            transition_id=f"T{i}",
            module_id=f"MODULE_{i:02d}",
            sequence_number=i,
            payload=p,
            previous_hash=prev,
        )
        receipts.append(r)
        prev = r["state_hash"]
    assert verify_ledger(receipts, payloads)["ok"] is True
