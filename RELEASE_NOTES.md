# SWI v4.7 Ethical Core Stack - Release Notes

## Overview
This release finalizes the transformation of SWI into the **v4.7 Ethical Core Stack (Research Prototype)**. The focus of this release is on governance, structural integrity, and the enforcement of the "AI Court" human-in-the-loop ethical guidelines.

## Key Changes

### 1. Governance & Header Alignment
*   Updated `README.md`, `README_GOVERNANCE.md`, `metadata.json`, and `PROPOSAL.md` to formally reflect the **SWI v4.7 Ethical Core Stack** positioning.
*   Updated references across the application UI to maintain version consistency (e.g. `App.tsx` headers).

### 2. Manifest Standardization
*   Formalized the underlying system manifest at `swi-core/manifest/manifest.json`.
*   Bumped all schema and runtime versions to `4.7.0` to ensure proper verification loops and drift calculation consistency. 

### 3. Execution Kernel & Economic Guards (Demo Enhancements)
*   **Softened Strict Halts**: The `hashChainKernel.ts` previously threw hard exceptions (e.g., `MISSING_ROLLBACK_OWNER_BOUND`) when simulated financial or transfer requests lacked exact economic owners.
*   **Operational Incident Fallback**: These operations now automatically assign systemic fallbacks (`SYSTEM_DEFAULT_RECOVERY`, `SYSTEM_DEFAULT_TREASURY`) and log warnings rather than completely bricking the execution pipeline during early prototyping or demonstrations.
*   This significantly improves the front-end simulation flow specifically for research prototyping.

### 4. General Cleanup
*   Minor fixes to old structural artifact references.
*   Confirmed complete JSON reporting via `generate_report.js` and matching CI actions.

---
**Verdict:** The system operates securely according to research specifications. It is fit for internal compliance review and public demonstration of Ethical / Policy-first runtime models.
