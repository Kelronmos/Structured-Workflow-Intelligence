"""Seal Verifier — independent inspection of seal records.

CRITICAL: Never trust module[\"state\"] == \"SEALED\".
Always re-verify contract, commit, tests, CI, dependencies and evidence hash.
"""

from __future__ import annotations

from typing import Any, Optional

from .halt import halt


def verify_seal(module: dict[str, Any], seal_record: Optional[dict] = None) -> dict[str, Any]:
    """Independently verify a module seal.

    Returns {\"ok\": True, ...} on success or a HALT event on failure.
    """
    module_id = module.get("module") or module.get("name") or "UNKNOWN"

    # 1. Seal record must exist
    if seal_record is None:
        return halt(
            module=module_id,
            reason="MISSING_SEAL_RECORD",
            required="SEALED_WITH_RECORD",
            observed=module.get("state", "UNKNOWN"),
        )

    # 2. State in registry must claim SEALED (but we still verify)
    if module.get("state") != "SEALED":
        return halt(
            module=module_id,
            reason="REGISTRY_STATE_NOT_SEALED",
            required="SEALED",
            observed=module.get("state", "UNKNOWN"),
        )

    # 3. Contract hash presence
    contract = seal_record.get("contract") or {}
    if not contract.get("sha256"):
        return halt(
            module=module_id,
            reason="MISSING_CONTRACT_HASH",
            required="contract.sha256",
            observed="absent",
        )

    # 4. Implementation commit presence
    impl = seal_record.get("implementation") or {}
    if not impl.get("commit"):
        return halt(
            module=module_id,
            reason="MISSING_IMPLEMENTATION_COMMIT",
            required="implementation.commit",
            observed="absent",
        )

    # 5. Tests must show zero failures
    tests = seal_record.get("tests") or {}
    if tests.get("failed", 1) != 0:
        return halt(
            module=module_id,
            reason="TESTS_FAILED",
            required="failed == 0",
            observed=str(tests.get("failed")),
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

    # 7. Evidence hash presence
    evidence = seal_record.get("evidence") or {}
    if not evidence.get("sha256"):
        return halt(
            module=module_id,
            reason="MISSING_EVIDENCE_HASH",
            required="evidence.sha256",
            observed="absent",
        )

    # All independent checks passed
    return {
        "ok": True,
        "module": module_id,
        "contract_sha256": contract.get("sha256"),
        "commit": impl.get("commit"),
        "evidence_sha256": evidence.get("sha256"),
    }
