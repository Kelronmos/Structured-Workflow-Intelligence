"""Tamper detection matrix."""

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from swi_core.crypto_audit import GENESIS_HASH, record_transition, verify_ledger, verify_receipt


def _chain():
    payloads = [{"amount": 500}, {"amount": 100}, {"amount": 50}]
    receipts = []
    prev = GENESIS_HASH
    for i, p in enumerate(payloads, start=1):
        r = record_transition(
            workflow_id="WF",
            transition_id=f"T{i}",
            module_id=f"MODULE_{i:02d}",
            sequence_number=i,
            payload=p,
            previous_hash=prev,
        )
        receipts.append(r)
        prev = r["state_hash"]
    return receipts, payloads


def test_payload_tamper():
    receipts, payloads = _chain()
    payloads[0] = {"amount": 501}
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False
    assert result["detail"]["reason"] == "PAYLOAD_HASH_MISMATCH"


def test_module_tamper():
    receipts, payloads = _chain()
    receipts[1] = copy.deepcopy(receipts[1])
    receipts[1]["module_id"] = "MODULE_99"
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False


def test_previous_hash_tamper():
    receipts, payloads = _chain()
    receipts[1] = copy.deepcopy(receipts[1])
    receipts[1]["previous_hash"] = "a" * 64
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False


def test_state_hash_tamper():
    receipts, payloads = _chain()
    receipts[0] = copy.deepcopy(receipts[0])
    receipts[0]["state_hash"] = "b" * 64
    result = verify_receipt(receipts[0], payload=payloads[0], expected_previous_hash=GENESIS_HASH)
    assert result["ok"] is False
    assert result["reason"] == "STATE_HASH_MISMATCH"


def test_deletion_breaks_chain():
    receipts, payloads = _chain()
    # delete middle
    del receipts[1]
    del payloads[1]
    # re-number not done — sequence gap
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False


def test_reordering_fails():
    receipts, payloads = _chain()
    receipts[1], receipts[2] = receipts[2], receipts[1]
    payloads[1], payloads[2] = payloads[2], payloads[1]
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False


def test_sequence_gap():
    receipts, payloads = _chain()
    receipts[1] = copy.deepcopy(receipts[1])
    receipts[1]["sequence_number"] = 99
    result = verify_ledger(receipts, payloads)
    assert result["ok"] is False
    assert result["reason"] == "SEQUENCE_GAP"
