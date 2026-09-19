"""Seal Verifier — independent inspection of seal records.

CRITICAL: Never trust module[\"state\"] == \"SEALED\".
Always re-verify contract, commit, tests, CI, dependencies and evidence hash.

This version moves from presence checks toward comparison checks.
Full cryptographic verification against live artifacts remains a later hardening step.
"""

from __future__ import annotations

from typing import Any, Optional

from .halt import halt


def verify_seal(
    module: dict[str, Any],
    seal_record: Optional[dict] = None,
    *,
    expected_contract_sha256: Optional[str] = None,
    expected_commit: Optional[str] = None,
) -> dict[str, Any]:
    """Independently verify a module seal.

    Returns {\"ok\": True, ...} on success or a HALT event on failure.
    """
    module_id = module.get("module") or module.get("name") or module.get("module_id") or "UNKNOWN"

    # 1. Seal record must exist — no warning path
    if seal_record is None:
        return halt(
            module=module_id,
            reason="MISSING_SEAL_RECORD",
            required="SEALED_WITH_RECORD",
            observed=module.get("state", "UNKNOWN"),
        )

    # 2. Registry state must claim SEALED (still not sufficient by itself)
    if module.get("state") != "SEALED":
        return halt(
            module=module_id,
            reason="REGISTRY_STATE_NOT_SEALED",
            required="SEALED",
            observed=module.get("state", "UNKNOWN"),
        )

    # 3. Contract hash must be present and, when expected value supplied, must match
    contract = seal_record.get("contract") or {}
    recorded_contract_sha = contract.get("sha256")
    if not recorded_contract_sha:
        return halt(
            module=module_id,
            reason="MISSING_CONTRACT_HASH",
            required="contract.sha256",
            observed="absent",
        )
    if expected_contract_sha256 is not None and recorded_contract_sha != expected_contract_sha256:
        return halt(
            module=module_id,
            reason="CONTRACT_HASH_MISMATCH",
            required=expected_contract_sha256,
            observed=recorded_contract_sha,
            contract_sha256=recorded_contract_sha,
        )

    # 4. Implementation commit must be present and, when expected value supplied, must match
    impl = seal_record.get("implementation") or {}
    recorded_commit = impl.get("commit")
    if not recorded_commit:
        return halt(
            module=module_id,
            reason="MISSING_IMPLEMENTATION_COMMIT",
            required="implementation.commit",
            observed="absent",
        )
    if expected_commit is not None and recorded_commit != expected_commit:
        return halt(
            module=module_id,
            reason="COMMIT_MISMATCH",
            required=expected_commit,
            observed=recorded_commit,
            commit=recorded_commit,
        )

    # 5. Tests must show zero failures
    tests = seal_record.get("tests") or {}
    failed = tests.get("failed", None)
    if failed is None:
        return halt(
            module=module_id,
            reason="MISSING_TEST_RESULTS",
            required="tests.failed == 0",
            observed="absent",
        )
    if failed != 0:
        return halt(
            module=module_id,
            reason="TESTS_FAILED",
            required="failed == 0",
            observed=str(failed),
        )

    # 6. CI conclusion must be success
    ci = seal_record.get("ci") or {}
    if ci.get("conclusion") != "success":
        return halt(
            module=module_id,
            reason="CI_NOT_SUCCESS",
            required="success",
            observed=str(ci.get("conclusion")),
        )

    # 7. Evidence hash must be present
    evidence = seal_record.get("evidence") or {}
    if not evidence.get("sha256"):
        return halt(
            module=module_id,
            reason="MISSING_EVIDENCE_HASH",
            required="evidence.sha256",
            observed="absent",
        )

    # All independent checks that are currently implemented have passed
    return {
        "ok": True,
        "module": module_id,
        "contract_sha256": recorded_contract_sha,
        "commit": recorded_commit,
        "evidence_sha256": evidence.get("sha256"),
        "note": "Seal metadata and comparison checks passed; full live artifact re-hash remains future hardening",
    }
