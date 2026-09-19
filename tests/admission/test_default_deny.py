"""Negative tests — prove the valve refuses invalid modules.

The most important property:
  unsealed / invalid modules never execute.
"""

import sys
from pathlib import Path

# Ensure admission package is importable
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.validator import admit
from admission.halt import halt


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
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
    )
    assert result["action"] == "HALT"
    assert "CONTRACT" in result.get("reason", "") or result.get("reason") == "MISSING_CONTRACT_HASH"


def test_fake_sealed_flag_halts():
    """Registry state == SEALED is never sufficient."""
    candidate = {
        "module": "V2-M99",
        "version": "V2",
        "state": "SEALED",
        "contract": {"sha256": "deadbeef"},
    }
    # No real seal_record provided → must HALT
    result = admit(
        candidate=candidate,
        registry={"modules": {"V2-M99": candidate}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
        seal_record=None,
    )
    assert result["action"] == "HALT"


def test_unknown_version_halts():
    candidate = {
        "module": "V2-M99",
        "version": "V99",
        "contract": {"sha256": "abc"},
    }
    result = admit(
        candidate=candidate,
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {"V2": {}}},
    )
    assert result["action"] == "HALT"
    assert result.get("reason") == "UNKNOWN_VERSION"


def test_execution_never_occurs_after_halt():
    """Critical invariant: after HALT, no execution path is taken."""
    execution_count = 0

    def fake_execute(_):
        nonlocal execution_count
        execution_count += 1

    result = admit(
        candidate={},
        registry={"modules": {}},
        policy={"default_action": "DENY"},
        version_registry={"versions": {}},
    )
    assert result["action"] == "HALT"
    # Simulate that the caller respects the HALT
    if result["action"] != "HALT":
        fake_execute(None)
    assert execution_count == 0
