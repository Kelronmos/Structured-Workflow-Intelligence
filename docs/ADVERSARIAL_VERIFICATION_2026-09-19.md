# SWI Adversarial Verification & Break Report

**Repository:** Kelronmos/Structured-Workflow-Intelligence  
**Commit tested:** 78196f2be483588ef31576766b350013d20ab096  
**Assessment at time of review:** FAILED / NOT VERIFIED / DO NOT PROMOTE  
**Date:** 2026-09-19

## Status after this commit

This commit applies the highest-priority structural fixes identified by the adversarial review:

1. **Execution-gate forgery** — hardened in `admission/execution_gate.py`
2. **M12 registry contradiction** — corrected in `config/swi-module-registry.json`
3. **Regression test** — `tests/admission/test_forged_admit_rejected.py`

The repository remains:

- **NOT SEALED**
- **EXECUTION AUTHORITY = DENIED**
- **DOWNSTREAM PROMOTION = DENIED**

until the full verification matrix is re-run green on the resulting tip.

## Critical findings (preserved)

### 1. Execution-gate forgery (FIXED in this commit)

Previous behaviour effectively did:

```python
if admission_result["action"] == "ADMIT":
    execute()
```

A caller supplying `{"event":"FAKE","module":"ATTACKER","action":"ADMIT"}` could reach execution.

**Remediation applied:** gate now requires:

- `event == "ADMISSION_GRANTED"`
- `action == "ADMIT"`
- non-empty `module`
- non-empty `checks` list (produced by the real validator)

Anything else → HALT / reason code.  
Full cryptographic provenance binding of the admission artifact remains future work.

### 2. M12 registry contradiction (FIXED in this commit)

`config/swi-module-registry.json` previously marked M12 as `SEALED` while every verification flag was `false` and notes said “Blocked until M11 INTEGRATION_READY”.

**Remediation applied:** M12 state set to `CONTRACT_FROZEN`. Notes updated.  
`SEALED ≠ AUTHORIZED ≠ EXECUTABLE`. Module number is not permission.

### 3. Route reconstruction failure (OPEN)

CI run 35456094963 failed on `tests/route/test_route_chain.py::test_reconstruct`.
Surrounding route tests (canonicalization, hashing, append-only, chain validation, tamper detection) passed.  
Do **not** mark the test xfail or remove it. Reproduce under the exact CI environment and repair without weakening the gate.

### 4. Seal metadata is not live artifact verification (ACKNOWLEDGED)

`seal_verifier.py` correctly states that full live artifact re-hashing is future hardening.  
`SEAL RECORD PRESENT ≠ ARTIFACT VERIFIED`.

### 5. SHA-256 input-type weaknesses (OPEN — next hardening)

- Hash length checked but hex encoding not strictly required.
- `isinstance(sequence_number, int)` accepts `bool` (subclass of int).

Required later:

- exact lowercase `[0-9a-f]{64}` validation
- reject `bool` for sequence numbers
- require non-empty string identifiers
- reject malformed receipts before hashing

## Required repair order (remaining)

1. Reproduce and diagnose `test_reconstruct` under CI conditions.
2. Add strict hash-format / type validation.
3. Add further adversarial cases (forged module ID, forged contract hash, forged predecessor, reordered/deleted route, stale seal, etc.).
4. Complete route suite → determinism → crypto audit → independent crypto verification → workflow/security inspection → registry consistency.
5. Re-run complete matrix; record commit SHA, CI run ID, evidence hashes.
6. Only then consider any seal decision.

## Core rules (unchanged)

```
PASSING TESTS ≠ SECURITY CERTIFICATION
HASH ≠ AUTHORITY
SEALED ≠ EXECUTABLE
MODULE NUMBER ≠ PERMISSION
NO VERIFIED PREDECESSOR PATH = NO WORKFLOW EXECUTION
FORGED ADMIT ≠ EXECUTABLE
MAPPED ≠ FROZEN ≠ SEALED ≠ AUTHORIZED
```

## Governance conclusion

The defensive controls already catch many mutations. The review also found a concrete execution-boundary bypass and a registry-state contradiction. Those are now structurally addressed. The correct next step is to re-run the full verification chain on this tip and preserve any remaining failures as evidence.
