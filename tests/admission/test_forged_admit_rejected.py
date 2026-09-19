"""Regression: forged ADMIT must never reach execution.

CRITICAL finding (2026-09-19 adversarial review):
Previous execution_gate accepted any dict with action==\"ADMIT\".
A caller could supply {\"event\":\"FAKE\",\"module\":\"ATTACKER\",\"action\":\"ADMIT\"}
and the side-effect would execute.

This test must remain mandatory. Do not xfail or remove it to obtain green CI.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.execution_gate import execute_if_admitted
from admission.validator import admit


def test_forged_admit_dictionary_cannot_execute():
    """Pure dictionary forgery must be rejected."""
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1
        return "SHOULD_NEVER_RUN"

    forged = {
        "event": "FAKE",
        "module": "ATTACKER",
        "action": "ADMIT",
    }
    outcome = execute_if_admitted(forged, fake_execute)
    assert outcome["executed"] is False
    assert execution_count == 0
    assert outcome["reason"] in (
        "MISSING_OR_WRONG_EVENT",
        "MISSING_OR_EMPTY_CHECKS",
        "ADMISSION_NOT_GRANTED",
        "FORGED_OR_INCOMPLETE_ADMISSION",
    )


def test_forged_admit_with_checks_still_requires_real_event():
    """Even if an attacker adds a checks list, wrong event must still block."""
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1

    forged = {
        "event": "ADMISSION_HALTED",  # wrong event
        "module": "ATTACKER",
        "action": "ADMIT",
        "checks": ["STRUCTURE", "CONTRACT"],
    }
    outcome = execute_if_admitted(forged, fake_execute)
    assert outcome["executed"] is False
    assert execution_count == 0


def test_missing_checks_blocks_execution():
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1

    incomplete = {
        "event": "ADMISSION_GRANTED",
        "module": "SOME-MODULE",
        "action": "ADMIT",
        # checks deliberately omitted
    }
    outcome = execute_if_admitted(incomplete, fake_execute)
    assert outcome["executed"] is False
    assert execution_count == 0
    assert outcome["reason"] == "MISSING_OR_EMPTY_CHECKS"


def test_halt_still_blocks_execution():
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
