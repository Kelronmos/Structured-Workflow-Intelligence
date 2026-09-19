# Cryptographic State Audit Contract

**component_id:** SWI-CRYPTO-AUDIT  
**contract_version:** 1.0-proposed  
**hash_algorithm:** SHA-256  
**status:** IMPLEMENTED_NOT_VERIFIED  
**Governance:** NOT SEALED

## Bounded claim

Where a transition is represented by a defined canonical payload and cryptographically linked to its predecessor, the resulting receipt chain can provide verifiable evidence of the recorded sequence and the integrity of the recorded representation.

## Not claimed

- factual truth
- AI safety
- regulatory compliance
- production readiness
- storage immutability
- non-repudiation
- execution purity
- Merkle-tree security
- replay protection
- identity authenticity

## Genesis

```
0000000000000000000000000000000000000000000000000000000000000000
```

## Domain separation

- `SWI-PAYLOAD-V1` — payload digests
- `SWI-CRYPTO-AUDIT-STATE-V1` — state transition digests

## Canonicalization

- UTF-8 JSON
- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=False`
- Supported: dict, list, str, int, bool, null
- Reject: float, set, bytes, custom objects, datetime, functions, etc. (no silent `str()`)

## State hash construction

```
state_hash = SHA-256(canonical({
  "domain": "SWI-CRYPTO-AUDIT-STATE-V1",
  "module_id": ...,
  "previous_hash": ...,
  "payload_hash": ...
}))
```

Timestamps and observational metadata MUST NOT enter the state hash.

## Receipt (deterministic state fields)

- receipt_version
- workflow_id
- transition_id
- module_id
- sequence_number
- payload_hash
- previous_hash
- state_hash

Metadata (optional, non-hashing): recorded_at

## Failure

Any mismatch → structured FAIL / HALT evidence. No silent continue.
