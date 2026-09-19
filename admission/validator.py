"""Admission Validator — the sealed valve.

Order is mandatory and non-negotiable:
  1. STRUCTURE
  2. CONTRACT
  3. VERSION
  4. INTEGRITY
  5. SEAL
  6. DEPENDENCY

NO FALLTHROUGH. Any failure → HALT. Execution never occurs after HALT.

Integrity is derived/compared, never merely asserted by the candidate.
"""

from __future__ import annotations

from typing import Any, Optional

from .halt import halt
from .seal_verifier import verify_seal
from .dependency_gate import check_dependencies


def validate_structure(candidate: dict) -> dict:
    if not isinstance(candidate, dict):
        return halt("UNKNOWN", "INVALID_STRUCTURE", "dict", type(candidate).__name__)
    if not candidate.get("module") and not candidate.get("module_id"):
        return halt("UNKNOWN", "MISSING_MODULE_ID", "module or module_id", "absent")
    return {"ok": True}


def validate_contract(candidate: dict) -> dict:
    contract = candidate.get("contract") or {}
    if not contract.get("sha256"):
        mid = candidate.get("module") or candidate.get("module_id") or "UNKNOWN"
        return halt(mid, "MISSING_CONTRACT_HASH", "contract.sha256", "absent")
    return {"ok": True}


def validate_version(candidate: dict, version_registry: dict) -> dict:
    version = candidate.get("version")
    if not version:
        mid = candidate.get("module") or "UNKNOWN"
        return halt(mid, "MISSING_VERSION", "version field", "absent")
    versions = version_registry.get("versions", {})
    if version not in versions:
        mid = candidate.get("module") or "UNKNOWN"
        return halt(mid, "UNKNOWN_VERSION", "registered version", str(version))
    return {"ok": True}


def validate_integrity(candidate: dict) -> dict:
    """Integrity must be derived or explicitly compared, never merely asserted.

    Accepted paths:
    - candidate supplies expected_commit + actual_commit and they match
    - candidate supplies expected_contract_sha256 + actual_contract_sha256 and they match
    - or both

    Forbidden:
    - integrity_verified: true   (assertion only)
    - missing integrity fields when policy requires them
    """
    mid = candidate.get("module") or candidate.get("module_id") or "UNKNOWN"

    # Reject pure assertion
    if "integrity_verified" in candidate and candidate.get("integrity_verified") is True:
        # Assertion alone is never sufficient
        if not (
            (candidate.get("expected_commit") and candidate.get("actual_commit"))
            or (candidate.get("expected_contract_sha256") and candidate.get("actual_contract_sha256"))
        ):
            return halt(
                mid,
                "INTEGRITY_ASSERTED_ONLY",
                "derived comparison (commit and/or contract hash)",
                "integrity_verified=True without comparison fields",
            )

    expected_commit = candidate.get("expected_commit")
    actual_commit = candidate.get("actual_commit")
    expected_csha = candidate.get("expected_contract_sha256")
    actual_csha = candidate.get("actual_contract_sha256")

    # At least one comparison pair must be present and match
    has_commit_pair = expected_commit is not None and actual_commit is not None
    has_contract_pair = expected_csha is not None and actual_csha is not None

    if not has_commit_pair and not has_contract_pair:
        return halt(
            mid,
            "INTEGRITY_FIELDS_MISSING",
            "expected/actual commit and/or contract hash pair",
            "absent",
        )

    if has_commit_pair and expected_commit != actual_commit:
        return halt(
            mid,
            "COMMIT_MISMATCH",
            str(expected_commit),
            str(actual_commit),
            commit=str(actual_commit),
        )

    if has_contract_pair and expected_csha != actual_csha:
        return halt(
            mid,
            "CONTRACT_HASH_MISMATCH",
            str(expected_csha),
            str(actual_csha),
            contract_sha256=str(actual_csha),
        )

    return {"ok": True}


def validate_seal(
    candidate: dict,
    seal_record: Optional[dict] = None,
) -> dict:
    return verify_seal(
        candidate,
        seal_record,
        expected_contract_sha256=candidate.get("expected_contract_sha256"),
        expected_commit=candidate.get("expected_commit") or candidate.get("actual_commit"),
    )


def validate_dependencies(
    candidate: dict,
    registry: dict,
    seal_records: Optional[dict] = None,
) -> dict:
    mid = candidate.get("module") or candidate.get("module_id") or "UNKNOWN"
    deps = candidate.get("dependencies") or candidate.get("required_dependencies") or []
    return check_dependencies(mid, deps, registry, seal_records)


def validate(
    candidate: dict,
    registry: dict,
    policy: dict,
    version_registry: Optional[dict] = None,
    seal_record: Optional[dict] = None,
    seal_records: Optional[dict] = None,
) -> dict:
    """Full validation sequence. Returns ADMIT evidence or HALT evidence."""
    version_registry = version_registry or {}

    # Policy itself must be present and default to DENY
    if not policy:
        return halt(
            candidate.get("module") or "UNKNOWN",
            "MISSING_POLICY",
            "policy object with default_action=DENY",
            "absent",
        )
    if policy.get("default_action") != "DENY":
        return halt(
            candidate.get("module") or "UNKNOWN",
            "POLICY_DEFAULT_NOT_DENY",
            "DENY",
            str(policy.get("default_action")),
        )

    # 1. STRUCTURE
    result = validate_structure(candidate)
    if not result.get("ok"):
        return result

    # 2. CONTRACT
    result = validate_contract(candidate)
    if not result.get("ok"):
        return result

    # 3. VERSION
    result = validate_version(candidate, version_registry)
    if not result.get("ok"):
        return result

    # 4. INTEGRITY (derived / compared)
    result = validate_integrity(candidate)
    if not result.get("ok"):
        return result

    # 5. SEAL
    result = validate_seal(candidate, seal_record)
    if not result.get("ok"):
        return result

    # 6. DEPENDENCY
    result = validate_dependencies(candidate, registry, seal_records)
    if not result.get("ok"):
        return result

    # All checks passed
    mid = candidate.get("module") or candidate.get("module_id")
    return {
        "event": "ADMISSION_GRANTED",
        "module": mid,
        "action": "ADMIT",
        "checks": ["STRUCTURE", "CONTRACT", "VERSION", "INTEGRITY", "SEAL", "DEPENDENCY"],
    }


def admit(
    candidate: dict,
    registry: dict,
    policy: dict,
    version_registry: Optional[dict] = None,
    seal_record: Optional[dict] = None,
    seal_records: Optional[dict] = None,
) -> dict:
    """Public admission entry point."""
    return validate(
        candidate=candidate,
        registry=registry,
        policy=policy,
        version_registry=version_registry,
        seal_record=seal_record,
        seal_records=seal_records,
    )
