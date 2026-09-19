"""Expanded negative admission matrix (SWI-GOV-REMEDIATION-001 §10)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from admission.validator import admit
from admission.execution_gate import execute_if_admitted

POLICY = {"default_action": "DENY"}
VERSIONS = {"versions": {"V2": {}}}


def _base_candidate(**overrides):
    c = {
        "module": "V2-M99",
        "version": "V2",
        "state": "SEALED",
        "contract": {"sha256": "abc123"},
        "expected_commit": "commit1",
        "actual_commit": "commit1",
        "expected_contract_sha256": "abc123",
        "actual_contract_sha256": "abc123",
        "dependencies": [],
    }
    c.update(overrides)
    return c


def test_missing_structure_halts():
    result = admit({}, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"


def test_missing_contract_halts():
    c = _base_candidate()
    del c["contract"]
    result = admit(c, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") == "MISSING_CONTRACT_HASH"


def test_unknown_version_halts():
    c = _base_candidate(version="V99")
    result = admit(c, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") == "UNKNOWN_VERSION"


def test_integrity_missing_halts():
    c = _base_candidate()
    del c["expected_commit"]
    del c["actual_commit"]
    del c["expected_contract_sha256"]
    del c["actual_contract_sha256"]
    result = admit(c, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") in ("INTEGRITY_FIELDS_MISSING", "INTEGRITY_ASSERTED_ONLY")


def test_integrity_mismatch_halts():
    c = _base_candidate(actual_commit="different")
    result = admit(c, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") == "COMMIT_MISMATCH"


def test_fake_integrity_flag_halts():
    c = _base_candidate(integrity_verified=True)
    # Remove comparison fields so assertion alone is tested
    del c["expected_commit"]
    del c["actual_commit"]
    del c["expected_contract_sha256"]
    del c["actual_contract_sha256"]
    result = admit(c, {"modules": {}}, POLICY, VERSIONS)
    assert result["action"] == "HALT"


def test_missing_seal_halts():
    c = _base_candidate()
    result = admit(c, {"modules": {"V2-M99": c}}, POLICY, VERSIONS, seal_record=None)
    assert result["action"] == "HALT"
    assert result.get("reason") == "MISSING_SEAL_RECORD"


def test_permissive_policy_halts():
    c = _base_candidate()
    result = admit(c, {"modules": {}}, {"default_action": "ALLOW"}, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") == "POLICY_DEFAULT_NOT_DENY"


def test_missing_policy_halts():
    c = _base_candidate()
    result = admit(c, {"modules": {}}, {}, VERSIONS)
    assert result["action"] == "HALT"
    assert result.get("reason") == "MISSING_POLICY"


def test_execution_gate_blocks_halt():
    counter = 0

    def run():
        nonlocal counter
        counter += 1

    halt_result = {"action": "HALT", "reason": "TEST"}
    outcome = execute_if_admitted(halt_result, run)
    assert outcome["executed"] is False
    assert counter == 0
