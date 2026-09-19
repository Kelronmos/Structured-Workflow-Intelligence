"""Negative tests — prove the valve refuses invalid modules."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.validator import admit
from admission.execution_gate import execute_if_admitted


def test_default_deny_empty_candidate():
    result = admit(
        candidate={},
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {}},
    )
    assert result["action"] == "HALT"


def test_missing_contract_halts():
    candidate = {
        "module": "V2-M99",
        "version": "V2",
        "state": "IMPLEMENTED",
        "expected_commit": "a",
        "actual_commit": "a",
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
    )
    assert result["action"] == "HALT"
    assert result.get("reason") == "MISSING_CONTRACT_HASH"


def test_fake_sealed_flag_halts():
    """Registry state == SEALED is never sufficient without a seal_record."""
    candidate = {
        "module": "V2-M99",
        "version": "V2",
        "state": "SEALED",
        "contract": {"sha256": "deadbeef"},
        "expected_commit": "c1",
        "actual_commit": "c1",
        "expected_contract_sha256": "deadbeef",
        "actual_contract_sha256": "deadbeef",
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {"V2-M99": candidate}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
        seal_record=None,
    )
    assert result["action"] == "HALT"
    assert result.get("reason") == "MISSING_SEAL_RECORD"


def test_integrity_asserted_only_halts():
    candidate = {
        "module": "V2-M99",
        "version": "V2",
        "state": "SEALED",
        "contract": {"sha256": "abc"},
        "integrity_verified": True,  # assertion only — forbidden
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
    )
    assert result["action"] == "HALT"
    assert result.get("reason") in ("INTEGRITY_ASSERTED_ONLY", "INTEGRITY_FIELDS_MISSING")


def test_unknown_version_halts():
    candidate = {
        "module": "V2-M99",
        "version": "V99",
        "contract": {"sha256": "abc"},
        "expected_commit": "c",
        "actual_commit": "c",
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
    )
    assert result["action"] == "HALT"
    assert result.get("reason") == "UNKNOWN_VERSION"


def test_execution_never_occurs_after_halt_via_gate():
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1

    result = admit(
        candidate={},
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {}},
    )
    assert result["action"] == "HALT"

    outcome = execute_if_admitted(result, fake_execute)
    assert outcome["executed"] is False
    assert execution_count == 0
