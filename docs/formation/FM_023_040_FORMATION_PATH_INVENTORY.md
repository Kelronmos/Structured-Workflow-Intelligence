# Formation Path Inventory — FM-023 … FM-040

**Package status:** `PROPOSED` · `NOT_IMPLEMENTED`  
**Proof status:** none  
**Seal status:** not applicable (no seal claimed or implied)  
**Date:** 2026-09-20  

## Authority of this document

This inventory is the **authoritative formation-path map** for the proposed Sandbox / SCAR / authority construction band.

It does **not**:

- assert that any path is implemented in V1, V2, or this repository;
- assert TESTED, VERIFIED, SEALED, AUTHORIZED, or EXECUTABLE;
- upgrade V1 FM-001–013 or V2 M11–M22 status.

```text
PROPOSED / NOT_IMPLEMENTED
≠ DOCUMENTED AS PROVEN
≠ SEALED
≠ AUTHORIZED
≠ EXECUTABLE
```

## Repository placement (intentional)

| Band | IDs | Home | Role |
|------|-----|------|------|
| Foundation formation | FM-001 … FM-013 | **V1** | Evidence / formation baseline only |
| Continuity / admission | M11 … M22 | **V2** | Downstream contracts |
| **This band** | **FM-023 … FM-040** | **V3 / construction (proposed)** — documented here until a construction repo exists | Sandbox, risk, safety, SCAR, authority, closure |
| External verification | S9 (out of band) | External | Independent verification — not claimed here |

**Do not implement FM-023–040 inside V1.**

## Five-axis separation (summary)

| Axis ID | Name | Establishes (when proven) | Does **not** establish |
|---------|------|---------------------------|-------------------------|
| A1 | `integrity` | Artifact / binding integrity under a defined rule | Truth, authority, path closure, legal compliance |
| A2 | `truth` | Factual correctness of world-claims | Integrity of packaging, authority, legal compliance |
| A3 | `authority` | Permission to decide or act under policy | Truth, integrity, path closure |
| A4 | `path_closure` | No residual ungoverned execution path for declared scope | Truth, legal compliance, universal safety |
| A5 | `legal_compliance` | Conformity to a cited normative instrument (when assessed) | Truth, operational authority, cryptographic integrity |

Schemas: `schemas/formation/swi-five-axis-separation.schema.json` and related.

## Formation path map

| ID | Name | Primary axes | Status |
|----|------|--------------|--------|
| FM-023 | Transaction Intake | A1 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-024 | Structure Validation | A1 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-025 | Evidence Binding | A1 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-026 | Sandbox Clone | A1 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-027 | Normative Mapping | A5 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-028 | Requirement Strength | A5 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-029 | Applicability | A5 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-030 | Risk Assessment | (risk model; not A3) | **PROPOSED / NOT_IMPLEMENTED** |
| FM-031 | Safety / Consequence Simulation | (safety model; not A3) | **PROPOSED / NOT_IMPLEMENTED** |
| FM-032 | Authority Determination | A3 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-033 | SCAR | structured control record | **PROPOSED / NOT_IMPLEMENTED** |
| FM-034 | SCARMATIC | SCAR packaging | **PROPOSED / NOT_IMPLEMENTED** |
| FM-035 | Human / Authorized Review | A3 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-036 | Control Decision | A3 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-037 | Evidence Closure | A1 | **PROPOSED / NOT_IMPLEMENTED** |
| FM-038 | Replay | reproducibility | **PROPOSED / NOT_IMPLEMENTED** |
| FM-039 | Adversarial Verification | attack tests | **PROPOSED / NOT_IMPLEMENTED** |
| FM-040 | Independent Verification | external / S9-style | **PROPOSED / NOT_IMPLEMENTED** |

```text
FM-023 → … → FM-040  (specification graph only; not executable in-repo)
```

## Non-claims

| Claim | Under this package |
|-------|--------------------|
| Any FM-023–040 implemented | **Not claimed** |
| Universal Gate proven | **NOT_PROVEN** (out of scope) |
| SCAR / SCARMATIC runtime | **NOT_IMPLEMENTED** |
| Sandbox execution authorized | **NOT_AUTHORIZED** |
| Production readiness | **NOT_CLAIMED** |

Machine index: `docs/formation/fm_023_040_inventory.json`.

**End.** Status remains **PROPOSED / NOT_IMPLEMENTED**.
