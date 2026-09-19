"""Dependency Gate — sealed valve.

For every required dependency:
  verify_seal(dependency)
  if not ok → HALT
"""

from __future__ import annotations

from typing import Any, Iterable

from .halt import halt
from .seal_verifier import verify_seal


def check_dependencies(
    module_id: str,
    required_dependencies: Iterable[str],
    registry: dict[str, Any],
    seal_records: dict[str, dict] | None = None,
) -> dict[str, Any]:
    """Verify every dependency is SEALED and independently verifiable."""
    seal_records = seal_records or {}

    for dep_id in required_dependencies:
        dep_module = registry.get("modules", {}).get(dep_id)
        if dep_module is None:
            return halt(
                module=module_id,
                reason="DEPENDENCY_NOT_IN_REGISTRY",
                required="present in MODULE_REGISTRY",
                observed="absent",
                dependency=dep_id,
            )

        result = verify_seal(dep_module, seal_records.get(dep_id))
        if not result.get("ok"):
            # Propagate the HALT with clearer reason
            return halt(
                module=module_id,
                reason="DEPENDENCY_NOT_SEALED",
                required="SEALED",
                observed=dep_module.get("state", "UNKNOWN"),
                dependency=dep_id,
                commit=result.get("commit"),
                contract_sha256=result.get("contract_sha256"),
            )

    return {"ok": True, "module": module_id, "dependencies_verified": list(required_dependencies)}
