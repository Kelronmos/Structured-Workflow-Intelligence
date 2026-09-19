# START HERE: SWI Reviewer Guide

> **Honesty banner:** This repository is a **research prototype** (`SWI_SYSTEM_STATE.json`: RESEARCH_PROTOTYPE / DO_NOT_DEPLOY).  
> Components may be REAL, HYBRID, or SIMULATED. Documentation is not verification.  
> Do not treat this guide as a production security certification.

## One-Paragraph Explanation

Structured Workflow Intelligence (SWI) explores a security-first **research** runtime pattern for AI agents: intercept requested actions, evaluate them against policy/manifest constraints, and record decisions for auditability. Some paths are implemented; others are simulated or partial. Always check module registry state and seal evidence before trusting any claim.

## Component List (as designed / partially present)

- **`app/`**: Frontend monitoring console (where present).
- **`core/kernel/`**: Decision logic (`SWIKernel`) — maturity varies by file.
- **`core/manifest/`**: Policy definition (`manifest.json`) — treat hashes/signatures as unverified unless evidence exists.
- **`core/keys/`**: Key material for local dev only; never assume production HSM/TPM.
- **`certification/`**: Research proof artifacts if present — not EU AI Act conformity.

## How to Run (local research)

1. **Install**: `npm install` (or `npm ci` when lockfile is authoritative)
2. **Start**: `npm run dev` (if configured)
3. **Access**: Open `http://localhost:3000` when the app serves
4. **Control plane**:
   ```bash
   node scripts/swi-verify-module.mjs
   node scripts/swi-seal.mjs
   ```

## Key Logic Locations (inspect, do not assume sealed)

- Manifest / policy paths under `core/` when present
- Audit / hash-chain logic under `core/kernel/` when present
- Registry: `config/swi-module-registry.json`
- Seal evidence: `evidence/` + `schemas/swi-seal-record.schema.json`

## Reviewer rules

1. EXISTS ≠ VERIFIED ≠ SEALED ≠ PRODUCTION READY  
2. A green local demo is not a seal.  
3. Prefer executable tests and seal records over narrative docs.  
4. Report vulnerabilities privately (see `SECURITY.md`).

---
*If the system is designed to HALT on tamper, that behavior must be demonstrated by tests — not asserted only in prose.*
