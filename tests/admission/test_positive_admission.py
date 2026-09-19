"""Positive admission fixture — proves the valve can grant ADMIT under correct conditions."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.validator import admit
from admission.execution_gate import execute_if_admitted


def test_valid_candidate_is_admitted():
    candidate = {
        "module": "TEST-MODULE",
        "module_id": "TEST-MODULE",
        "version": "V2",
        "state": "SEALED",
        "contract": {"sha256": "abc123contract"},
        "expected_commit": "deadbeefcommit",
        "actual_commit": "deadbeefcommit",
        "expected_contract_sha256": "abc123contract",
        "actual_contract_sha256": "abc123contract",
        "dependencies": [],
    }

    seal_record = {
        "contract": {"sha256": "abc123contract"},
        "implementation": {"commit": "deadbeefcommit"},
        "tests": {"total": 1, "passed": 1, "failed": 0},
        "ci": {"workflow": "governance.yml", "run_id": "1", "conclusion": "success"},
        "evidence": {"sha256": "evidencehash"},
    }

    registry = {"modules": {"TEST-MODULE": candidate}}
    version_registry = {"versions": {"V2": {}}}
    policy = {"default_action": "DENY"}

    result = admit(
        candidate=candidate,
        registry=registry,
        policy=policy,
        version_registry=version_registry,
        seal_record=seal_record,
        seal_records={},
    )

    assert result["action"] == "ADMIT"
    assert result["event"] == "ADMISSION_GRANTED"


def test_execution_gate_blocks_on_halt():
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1
        return "should-not-run"

    halt_result = {
        "event": "ADMISSION_HALTED",
        "module": "TEST-MODULE",
        "action": "HALT",
        "reason": "MISSING_SEAL_RECORD",
    }

    outcome = execute_if_admitted(halt_result, fake_execute)
    assert outcome["executed"] is False
    assert execution_count == 0


def test_execution_gate_allows_on_admit():
    execution_count = 0

    def fake_execute():
        nonlocal execution_count
        execution_count += 1
        return "ran"

    admit_result = {
        "event": "ADMISSION_GRANTED",
        "module": "TEST-MODULE",
        "action": "ADMIT",
    }

    outcome = execute_if_admitted(admit_result, fake_execute)
    assert outcome["executed"] is True
    assert execution_count == 1
    assert outcome["result"] == "ran"
