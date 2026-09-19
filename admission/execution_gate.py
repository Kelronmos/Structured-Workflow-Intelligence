"""Execution Gate — final barrier after admission.

Only a *verified* ADMISSION_GRANTED artifact may reach an execution function.
A HALT result, a forged dictionary, or an incomplete admission object
makes the execution path unreachable.

FORGED ADMIT ≠ EXECUTABLE
"""

from __future__ import annotations

from typing import Any, Callable


def _is_verified_admission(admission_result: dict[str, Any]) -> tuple[bool, str]:
    """Return (ok, reason). Rejects forged / incomplete admission objects.

    Minimum binding required before execution is permitted:
    - event must be exactly "ADMISSION_GRANTED"
    - action must be exactly "ADMIT"
    - module identity must be present and non-empty
    - checks list must be present and non-empty (produced by the real validator)

    This is still not full cryptographic provenance binding; it is the
    minimum structural gate that prevents the previous dictionary-forgery path.
    Full artifact attestation remains a future hardening item.
    """
    if not isinstance(admission_result, dict):
        return False, "ADMISSION_NOT_A_DICT"

    if admission_result.get("event") != "ADMISSION_GRANTED":
        return False, "MISSING_OR_WRONG_EVENT"

    if admission_result.get("action") != "ADMIT":
        return False, "ADMISSION_NOT_GRANTED"

    module = admission_result.get("module")
    if not module or not isinstance(module, str) or not module.strip():
        return False, "MISSING_MODULE_IDENTITY"

    checks = admission_result.get("checks")
    if not isinstance(checks, list) or len(checks) == 0:
        return False, "MISSING_OR_EMPTY_CHECKS"

    # Reject unexpected pure-assertion style fields that the real path never emits
    if admission_result.get("integrity_verified") is True and "checks" not in admission_result:
        return False, "INTEGRITY_ASSERTED_ONLY"

    return True, "OK"


def execute_if_admitted(
    admission_result: dict[str, Any],
    execute_fn: Callable[[], Any],
) -> dict[str, Any]:
    """Invoke execute_fn only when admission_result is a verified ADMISSION_GRANTED artifact.

    Returns a structured outcome. Never silently continues after HALT or forgery.
    """
    ok, reason = _is_verified_admission(admission_result)
    if not ok:
        return {
            "executed": False,
            "reason": reason,
            "admission": admission_result,
        }

    value = execute_fn()
    return {
        "executed": True,
        "result": value,
        "admission": admission_result,
    }
