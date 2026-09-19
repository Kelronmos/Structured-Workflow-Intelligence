#!/usr/bin/env python3
"""Independent verification entry for SWI-CRYPTO-AUDIT.

Does not authorize seal. Emits evidence + SHA-256.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from swi_core.crypto_audit import GENESIS_HASH, record_transition, verify_ledger


def main() -> int:
    out_dir = ROOT / "evidence" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    payloads = [{"step": 1}, {"step": 2}, {"step": 3}]
    receipts = []
    prev = GENESIS_HASH
    for i, p in enumerate(payloads, start=1):
        r = record_transition(
            workflow_id="WF-VERIFY",
            transition_id=f"T{i}",
            module_id=f"MODULE_{i:02d}",
            sequence_number=i,
            payload=p,
            previous_hash=prev,
        )
        receipts.append(r)
        prev = r["state_hash"]

    chain = verify_ledger(receipts, payloads)

    # Tamper check
    tampered_payloads = list(payloads)
    tampered_payloads[1] = {"step": 999}
    tamper = verify_ledger(receipts, tampered_payloads)

    evidence = {
        "verification_id": "SWI-CRYPTO-AUDIT-VERIFY",
        "component": "SWI-CRYPTO-AUDIT",
        "contract_version": "1.0-proposed",
        "repository": "Kelronmos/Structured-Workflow-Intelligence",
        "result": "PASS" if chain.get("ok") and not tamper.get("ok") else "FAIL",
        "nominal_chain": chain,
        "tamper_detection": {"ok_expected_false": tamper.get("ok"), "detail": tamper},
        "limitations": [
            "Does not establish factual truth",
            "Does not establish storage immutability",
            "Does not provide non-repudiation",
            "Does not provide replay protection",
            "SHA-256 hash chain, not Merkle tree",
            "Governance Backbone remains NOT SEALED",
        ],
    }

    payload = json.dumps(
        {k: v for k, v in evidence.items() if k != "verification_sha256"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    evidence["verification_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    out = out_dir / "crypto_audit_verification.json"
    out.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"crypto_audit: {evidence['result']} sha256={evidence['verification_sha256']}")
    return 0 if evidence["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
