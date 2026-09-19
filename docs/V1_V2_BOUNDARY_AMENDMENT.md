# V1–V2 Boundary Integration Amendment

**Date:** 2026-09-19  
**Authority:** Governance Authority  
**Status:** BINDING AMENDMENT — NOT SEALED

## Critical rule

Do **not** replace or bypass the existing boundary with a parallel protocol
(`Module10BoundaryExporter`, `Module11OrchestratorReceiver`, or similar)
unless that protocol is formally contracted, implemented, tested, independently
verified, and admitted through governance.

## Authoritative architecture (actual repositories)

```
V1 Trainer
    ↓
PipelineResult
    ↓
export_foundation_evidence()
    ↓
FoundationEvidenceEnvelope
    ↓
V2 M11 admit_foundation_input()
    ↓
AdmittedInput
    ↓
post-admission seal
    ↓
Kernel
```

**Repositories (canonical, no tracking parameters):**

- https://github.com/Kelronmos/SWI-V1-Module-1-10
- https://github.com/Kelronmos/SWI-V2-Modules-11-22
- https://github.com/Kelronmos/Structured-Workflow-Intelligence

**V2 implementation anchors (evidence from code search):**

- `swi_v2/kernel/admission.py` — `admit_foundation_input`, `compute_integrity_reference`
- `swi_v2/kernel/contracts.py` — `AdmittedInput`, `FoundationEvidenceEnvelope`
- `swi_v2/kernel/seal.py` — post-admission seal path
- `test/test_m11_post_admission_seal.py` — adversarial matrix against real types

## Three separate controls (do not conflate)

| Control | Purpose |
|---------|---------|
| A — Boundary integrity | Detect alteration of represented V1 evidence at M11 admission |
| B — State audit receipts | Reproducible SHA-256 integrity evidence for recorded transitions (SWI-CRYPTO-AUDIT) |
| C — Governance admission | Whether an object may cross a governed execution boundary |

None substitutes for another. Receipt ≠ authorization. Hash ≠ truth.

## Claim corrections (mandatory)

### Rejected language

- “every input payload is verified” (global guarantee from one test)
- “immutable execution ledger” from SHA-256 chaining alone
- “Merkle Ledger” for a simple previous-hash chain
- Parallel Module 10/11 exporters presented as the production boundary

### Approved bounded language

SWI defines explicit validation, admission, integrity and evidence boundaries for
governed transitions. Guarantees are limited to contracts and verification
evidence actually implemented.

Where explicitly implemented and independently verified, SWI can produce
SHA-256-linked state receipts that provide **reproducible integrity evidence**
for recorded transitions and predecessor relationships. The hash chain does
**not** establish immutable storage, non-repudiation, replay protection,
factual truth, or regulatory compliance.

## Zip / prototype diagnosis (2026-09-19)

Archive `swi-v4_-regulated-platform-intelligence (86).zip` is a **research
prototype / UI stack** (TypeScript components, experimental Merkle/ZK mocks).
It is **not** the V1 FoundationEvidenceEnvelope → V2 M11 production boundary.

Do not treat prototype README maturity tables or mock ZK/Merkle artifacts as
evidence for the governed V1→V2 handoff.

## Integration testing rule

```
BUILD THE TEST AROUND THE ACTUAL CONTRACT
— not around a convenient mock envelope.
```

Positive/negative/execution-gate tests for the boundary belong in
**SWI-V2-Modules-11-22** (and V1 producer fixtures), using real
`FoundationEvidenceEnvelope` / `admit_foundation_input` / `AdmittedInput`.

Governance Backbone may host claim/status registries and crypto-audit
primitives; it must not invent a second authoritative handoff.

## Current disposition

```
module_10_11_integration:
  parallel_protocol: NOT_AUTHORIZED
  actual_contract_path: FoundationEvidenceEnvelope → M11
  implementation_verification: DELEGATED_TO_V2_REPO
  cryptographic_zero_drift: NOT_CLAIMED
  execution_gate_on_backbone: PARTIAL (local admit valve only)

governance_backbone:
  state: NOT_SEALED
  execution_authority: DENIED
  m12_authorization: DENIED
```
