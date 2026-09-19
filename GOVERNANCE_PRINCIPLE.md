# SWI GOVERNANCE PRINCIPLE

**Existence does not grant authority.**

A module may execute only when its structure, contract, version, integrity, seal and dependencies have been independently verified.

The default state is **DENY**.

A failed verification produces **HALT** evidence.

No failed candidate may continue execution.

No README, status flag, branch name, module number, version declaration or developer assertion constitutes a seal.

**Evidence must precede authority.**  
**Verification must precede admission.**  
**Admission must precede execution.**

---

## Control Path

```
STRUCTURE
    ↓
CONTRACT
    ↓
IMPLEMENTATION
    ↓
TEST
    ↓
CI VERIFICATION
    ↓
AUDIT
    ↓
SEAL
    ↓
DEPENDENCY APPROVAL
    ↓
ADMISSION
    ↓
EXECUTION
```

Any failed condition → HALT (JSON + evidence + hash).

## State Distinctions (Mandatory)

- DECLARED_ONLY ≠ IMPLEMENTED
- IMPLEMENTED ≠ SEALED
- SEALED ≠ RELEASED
- Naming / association with “SWI” ≠ authority
