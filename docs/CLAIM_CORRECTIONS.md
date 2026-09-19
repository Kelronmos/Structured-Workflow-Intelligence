# Claim Corrections Registry

| ID | Rejected claim | Corrected claim | Evidence basis |
|----|----------------|-----------------|----------------|
| CC-001 | Every input payload is verified | Guarantees limited to implemented contracts + verification evidence | Amendment 2026-09-19 |
| CC-002 | Immutable execution ledger via hash chain | Tamper-evident SHA-256 hash chain; storage immutability not claimed | CRYPTO contract 1.0-proposed |
| CC-003 | Merkle ledger (simple prev-hash chain) | SHA-256 hash chain; Merkle not implemented in crypto_audit | swi_core/crypto_audit.py |
| CC-004 | Module10BoundaryExporter is the V1→V2 boundary | Boundary is FoundationEvidenceEnvelope → M11 admit | V1/V2 repos |
| CC-005 | Prototype zip = production SWI boundary | Zip is research UI/prototype; not V1/V2 handoff | zip inspection 2026-09-19 |
| CC-006 | Green pytest = SEALED | Seal requires full evidence chain + formal decision | SWI-GOV-REMEDIATION-* |

Status values for any feature: DOCUMENTED | IMPLEMENTED | TESTED | VERIFIED | SEALED  
Never mark SEALED without seal record + independent verification.
