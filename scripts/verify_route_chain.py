#!/usr/bin/env python3
"""verify_route_chain.py — load, validate, recompute hashes, verify chain, emit evidence.

Exit non-zero on failure. Does not claim SEALED.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from admission.route_chain import verify_route_chain, verify_route_record
from admission.route_store import RouteStore


def main() -> int:
    store_dir = ROOT / "evidence" / "routes"
    out_dir = ROOT / "evidence" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    store = RouteStore(store_dir)
    records = list(store.iter_records())

    # Sort by filename for stable ordering when parent links exist
    # Prefer parent-chain order if possible; otherwise sorted by route_id
    records.sort(key=lambda r: r.get("route_id", ""))

    individual = []
    for rec in records:
        individual.append(verify_route_record(rec))

    chain = verify_route_chain(records)

    evidence = {
        "verification_id": "GOV-ROUTE-VERIFY",
        "repository": "Kelronmos/Structured-Workflow-Intelligence",
        "operation": "verify_route_chain",
        "result": "PASS" if chain.get("ok") and all(i.get("ok") for i in individual) else "FAIL",
        "route_count": len(records),
        "chain": chain,
        "individual": individual,
        "limitations": [
            "Skeleton store; not a production append-only ledger",
            "Governance Backbone remains NOT SEALED",
        ],
    }

    payload = json.dumps(evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    evidence["verification_sha256"] = digest

    out_path = out_dir / "route_verification.json"
    out_path.write_text(
        json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    print(f"route_verification: {evidence['result']} count={len(records)} sha256={digest}")
    return 0 if evidence["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
