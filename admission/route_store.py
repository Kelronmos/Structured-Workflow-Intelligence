"""Append-only route store (SWI-GOV-REMEDIATION-002 §9).

No UPDATE / DELETE / OVERWRITE of historical records.
Corrections must be new records that reference prior routes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, List, Optional


class AppendOnlyViolation(RuntimeError):
    pass


class RouteStore:
    def __init__(self, root: str | Path = "evidence/routes"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, route_id: str) -> Path:
        # Simple file-per-record; production may replace with stronger store
        safe = route_id.replace("/", "_").replace("..", "_")
        return self.root / f"{safe}.json"

    def exists(self, route_id: str) -> bool:
        return self._path(route_id).exists()

    def write(self, route_id: str, record: dict[str, Any]) -> Path:
        path = self._path(route_id)
        if path.exists():
            raise AppendOnlyViolation(
                f"Route record already exists (append-only): {route_id}"
            )
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        path.write_text(canonical + "\n", encoding="utf-8")
        return path

    def read(self, route_id: str) -> dict[str, Any]:
        path = self._path(route_id)
        if not path.exists():
            raise FileNotFoundError(f"Route not found: {route_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_ids(self) -> List[str]:
        return sorted(p.stem for p in self.root.glob("*.json"))

    def iter_records(self) -> Iterator[dict[str, Any]]:
        for rid in self.list_ids():
            yield self.read(rid)
