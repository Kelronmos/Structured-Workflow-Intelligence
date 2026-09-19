# V1→V2 Boundary Integration Amendment

**Document:** SWI Boundary Technical Amendment  
**Date:** 2026-09-19  
**Status:** GOVERNANCE AMENDMENT  
**Governance Backbone:** NOT SEALED  
**Execution authority:** DENIED

---

## 1. Critical architecture rule

The governed V1→V2 boundary is:

```
V1 Trainer
    ↓
PipelineResult
    ↓
export_foundation_evidence()
    ↓
FoundationEvidenceEnvelope
    ↓
V2 M11 admission
    ↓
AdmittedInput
    ↓
post-admission seal
    ↓
Kernel
```

**Do not** replace or bypass this with:

- `Module10BoundaryExporter`
- `Module11OrchestratorReceiver`
- custom parallel envelopes
- mock/simulation handoffs

unless that alternate protocol is separately contracted, implemented, tested, independently verified, and admitted through governance.

A design experiment is not production boundary evidence.

---

## 2. Three controls remain separate

| Control | Purpose |
|---------|---------|
| **A — Boundary integrity** | Detect alteration of represented V1 evidence before/at M11 |
| **B — State audit receipts** | SHA-256 linked receipts for recorded transitions (tamper-evident, not immutable storage) |
| **C — Governance admission** | Identity → auth → contract → integrity → seal → dependency → ADMIT/HALT |

None substitutes for another. Receipt ≠ authorization. Hash ≠ truth.

---

## 3. Claim corrections

### Forbidden overclaim

> guaranteeing that every input payload is verified

### Corrected

SWI defines explicit validation, admission, integrity and evidence boundaries for governed transitions. Guarantees are limited to contracts and verification evidence actually implemented at a verified commit.

### Forbidden cryptographic language

> immutable execution ledger

### Corrected

Where implemented and independently verified, SWI can produce SHA-256-linked state receipts that provide **tamper-evident** integrity evidence for recorded transitions and predecessor relationships. This does **not** establish immutable storage, non-repudiation, replay protection, factual truth, or regulatory compliance.

---

## 4. Diagnosis of attached package (zip 86)

Source inspected: `swi-v4_-regulated-platform-intelligence (86).zip`

Findings:

- Package self-describes as **research prototype**, not production.
- README maturity table includes **ZK Proofs: Mock / Research**, Merkle/PKI experimental.
- `boundary.ts` contains mid-execution path marked simulate-style checkpoint validation.
- `ReceiptLayer.ts` uses `Date.now()` timestamps and does not implement the frozen Python `SWI-CRYPTO-AUDIT` contract.
- Multiple parallel crypto/Merkle/ZK modules exist; they are **not** automatic proof of the V1 FoundationEvidenceEnvelope → M11 path.

**Disposition:** Learn structure; do **not** treat zip contents as verified V1→V2 admission evidence or as authorization to seal.

Classification:

```
zip_package:
  type: RESEARCH_PROTOTYPE_ARTIFACT
  production_boundary_proof: false
  mock_or_simulation_present: true
  admissible_as_M11_evidence: false
```

---

## 5. Where real integration tests must live

| Concern | Repository |
|---------|------------|
| Foundation evidence production | https://github.com/Kelronmos/SWI-V1-Module-1-10 |
| M11 admission / AdmittedInput | https://github.com/Kelronmos/SWI-V2-Modules-11-22 |
| Governance registry, HALT, route, workflow gate, crypto-audit primitive | https://github.com/Kelronmos/Structured-Workflow-Intelligence |

Integration tests that claim M11 admission **must** execute against the real V2 implementation and real FoundationEvidenceEnvelope artifacts—not mocks in the governance backbone alone.

This repository may hold:

- contracts
- claim boundaries
- crypto-audit primitive (`swi_core/crypto_audit.py`)
- governance admission valve
- evidence schemas

It must **not** invent a second handoff protocol to greenwash tests.

---

## 6. Required test properties (when run on real V2)

Positive:

- valid FoundationEvidenceEnvelope → ADMITTED / AdmittedInput
- evidence_id, foundation_version, schema version, source_reference, integrity_reference preserved
- admitted_by from actual admission mechanism

Negative:

- raw dict → REJECT
- tampered payload → REJECT + execution_count == 0
- tampered integrity_reference → REJECT/HALT
- unknown foundation/schema version → REJECT
- each missing mandatory field → REJECT

Determinism / crypto (where contracted):

- canonical key-order independence
- previous_hash participates in state_hash
- full tamper matrix on receipt chain

Isolation:

- V2 tests without importing V1 runtime (`swi_core` unavailable unless contracted)
- no PYTHONPATH bypass as evidence of isolation

Terminology:

- `payload_mutation_by_receiver: NOT_DETECTED` — not “payload is immutable”

---

## 7. Status table (evidence-based)

| Component | State | Notes |
|-----------|-------|-------|
| V1 foundation evidence | EXTERNAL_REPO | Verify in SWI-V1-Module-1-10 |
| M11 admission | EXTERNAL_REPO | Verify in SWI-V2-Modules-11-22; do not claim SEALED here without seal record |
| M12 normalization | CONTRACT_FROZEN / BLOCKED | Implementation not started under backbone |
| Crypto state audit (this repo) | IMPLEMENTED_NOT_VERIFIED | Contract 1.0-proposed; tests present; not sealed |
| Policy 003 runtime | PARTIAL | Recorder/chain skeleton; not fully verified |
| Workflow activation | DENIED_UNLESS_VERIFIED | Legacy YAMLs not activated |
| Governance Backbone | NOT_SEALED | |
| Module 10→11 parallel exporter protocol | NOT_AUTHORIZED | |

---

## 8. Bounded acceptable claims after real verification

Boundary (when verified on actual commits):

> The SWI V1→V2 integration boundary provides reproducible verification of the explicitly contracted state handoff, including required structural validation, integrity checks, provenance preservation and rejection of specified tampering conditions, at the verified commit and CI boundary.

Crypto audit (when sealed):

> The SWI cryptographic state-audit component provides reproducible SHA-256 integrity evidence for explicitly recorded, canonically serialized state transitions and their predecessor relationships, when independently verified against the defined contract.

Neither claims truth, immutability, non-repudiation, replay protection, AI safety, legal compliance, or production readiness without separate evidence.

---

## 9. Implementation rule

```
DO NOT BUILD THE TEST AROUND THE CLAIM.
BUILD THE TEST AROUND THE ACTUAL CONTRACT.

CLAIM → CONTRACT → ACTUAL IMPLEMENTATION → TEST → CI → EVIDENCE → HASH → INDEPENDENT VERIFICATION → SEAL
```

Passing a mock test is not evidence for an architecture the repositories do not implement.
