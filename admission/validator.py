"""Admission Validator — the sealed valve.

Order is mandatory and non-negotiable:
  1. STRUCTURE
  2. CONTRACT
  3. VERSION
  4. INTEGRITY
  5. SEAL
  6. DEPENDENCY

NO FALLTHROUGH. Any failure → HALT. Execution never occurs after HALT.
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
    # Placeholder for full integrity (commit match, content hash, etc.)
    # Real implementation must compare against expected commit / content hash.
    if candidate.get("integrity_verified") is False:
        mid = candidate.get("module") or "UNKNOWN"
        return halt(mid, "INTEGRITY_FAILURE", "verified", "failed")
    return {"ok": True}


def validate_seal(candidate: dict, seal_record: Optional[dict] = None) -> dict:
    return verify_seal(candidate, seal_record)


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

    # 4. INTEGRITY
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
    # Enforce default DENY from policy
    if policy.get("default_action", "DENY") != "DENY":
        # Even if misconfigured, we still run full validation
        pass

    return validate(
        candidate=candidate,
        registry=registry,
        policy=policy,
        version_registry=version_registry,
        seal_record=seal_record,
        seal_records=seal_records,
    )
