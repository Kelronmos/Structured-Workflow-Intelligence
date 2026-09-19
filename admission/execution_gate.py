"""Execution Gate — final barrier after admission.

Only an ADMIT result may reach an execution function.
A HALT result makes the execution path unreachable.
"""

from __future__ import annotations

from typing import Any, Callable


def execute_if_admitted(
    admission_result: dict[str, Any],
    execute_fn: Callable[[], Any],
) -> dict[str, Any]:
    """Invoke execute_fn only when admission_result[\"action\"] == \"ADMIT\".

    Returns a structured outcome. Never silently continues after HALT.
    """
    if admission_result.get("action") != "ADMIT":
        return {
            "executed": False,
            "reason": "ADMISSION_NOT_GRANTED",
            "admission": admission_result,
        }

    value = execute_fn()
    return {
        "executed": True,
        "result": value,
        "admission": admission_result,
    }
