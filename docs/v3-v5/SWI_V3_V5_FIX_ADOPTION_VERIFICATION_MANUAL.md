# SWI v3–v5 Fix, Adoption, Verification & Sealed-Integration Manual

**Repository:** Kelronmos/Structured-Workflow-Intelligence  
**Companion process:** [SWI_V3_V4_V5_BUILD_MANUAL.md](../../SWI_V3_V4_V5_BUILD_MANUAL.md)  
**Controls:** `config/swi-module-registry.json` · `scripts/swi-verify-module.mjs` · `tests/swi-module-registry.test.mjs`  
**System honesty:** `SWI_SYSTEM_STATE.json` (research prototype where stated — do not invent production readiness)

---

## Mission

Not a rebuild. The objective is to:

1. discover what already exists;  
2. prove what already works;  
3. repair incomplete implementations;  
4. reuse mature infrastructure;  
5. add only genuinely missing capabilities;  
6. establish verification paths;  
7. seal every module until its path is proven;  
8. connect modules only after individual evidence passes;  
9. perform system-level verification after integration.  

**No module receives trust merely because its source code exists.**

---

## Golden rule

```text
Does SWI already have this?
  ├── YES → verified? ├── YES → ADOPT
  │                   └── NO  → FIX + VERIFY
  └── NO  → mature external system?
              ├── YES → ADAPTER
              └── NO  → BUILD
```

Never start with “How do we build this?”  
Start with “What do we already have, and what evidence proves it?”

---

## Operating path

```text
DISCOVER → ADOPT → AUDIT → FIX → EXTEND
  → BUILD ONLY WHAT IS MISSING → TEST → VERIFY → SEAL
  → PROVE INTEGRATION → CONNECT → SYSTEM VERIFY
```

Forbidden path: `REBUILD → CONNECT → HOPE → VERIFY`

---

## State transitions (no jumps)

```text
PLANNED → … → IMPLEMENTED → TESTED → VERIFIED → SEALED
  → INTEGRATION-READY → INTEGRATED → SYSTEM-VERIFIED
  → RELEASE-CANDIDATE → RELEASED
```

**Never:** `IMPLEMENTED → RELEASED`

### Vocabulary (mandatory)

```text
EXISTS ≠ VERIFIED
TESTED ≠ VERIFIED
VERIFIED ≠ INTEGRATED
INTEGRATED ≠ SYSTEM-VERIFIED
SYSTEM-VERIFIED ≠ RELEASED
```

Avoid unsupported: DONE / COMPLETE / SECURE / PRODUCTION READY / FULLY HARDENED / 100%.

---

## Classification

| Disposition | When |
|-------------|------|
| **ADOPT** | Contract met, security acceptable, tests sufficient |
| **FIX / HARDEN** | Exists but defective or under-verified |
| **EXTEND** | Foundation correct, features missing |
| **ADAPTER** | Mature external system; SWI owns identity/policy/audit/verification |
| **BUILD** | Absent and no suitable external option |
| **DEFER** | Not safely definable yet (owner + criteria required) |

---

## Seal levels

| Level | Meaning | Production |
|-------|---------|------------|
| SEAL-0 | Contract only | Prohibited |
| SEAL-1 | Implementation + unit tests | Prohibited |
| SEAL-2 | Verification path (unit/negative/security/determinism as applicable) | Prohibited until INTEGRATION-READY |
| SEAL-3 | System verification | Release-candidate path only |

---

## Repository controls (live)

```bash
# Registry consistency + dependency / production_ready gates
node scripts/swi-verify-module.mjs
node scripts/swi-verify-module.mjs M11

# Automated assertions (M11/M12 sealed, no production_ready)
node --test tests/swi-module-registry.test.mjs
```

**Registry rules (enforced in script):**

- `production_ready=true` requires unit + negative + security flags **and** a trusted state  
- `integration_enabled=true` requires state ∈ {INTEGRATION_READY, SYSTEM_VERIFIED, RELEASED}  
- SEALED cannot set `integration_enabled=true`  
- Dependencies must exist; integrated modules cannot depend on untrusted deps  

**Do not** flip verification flags to `true` by hand because code “looks done.” Flags track evidence.

Optional inventory worksheet: create `docs/v3-v5/CAPABILITY_INVENTORY.md` when performing a full baseline (do not invent rows without inspection).

---

## M11 before M12

```text
M11 DISCOVER → ADOPT → FIX → TEST → VERIFY → SEAL → INTEGRATION-READY
                              ↓
                         M12 DISCOVER → … → INTEGRATION-READY
                              ↓
                    joint integration → system verify
```

**Current registry (control plane):** M11 and M12 are **SEALED**, `integration_enabled=false`, `production_ready=false`.

M11 focuses on security/admission/verification foundations (align with V2 M11 admission where applicable).  
M12 focuses on operational maturity only **after** M11 is INTEGRATION-READY with evidence.

---

## Fix loop

```text
IDENTIFY → REPRODUCE → FAILING TEST → FIX
  → targeted tests → module tests → regression
  → security → determinism → VERIFY
```

Security defects: add a reproducible test when practical before claiming the fix.

---

## Integration & rollout

INTEGRATION-READY only when applicable gates pass: contract, unit, negative, determinism, security, dependencies, integration tests.

Rollout: DISABLED → SHADOW → TEST → CANARY → CONTROLLED → GENERAL.  
Rollback defined and tested **before** activation.

---

## Absolute integration rule

```text
UNVERIFIED MODULE  →  PRODUCTION     must be mechanically blocked
```

Allowed path only:

```text
IMPLEMENTED → TESTED → VERIFIED → SEALED
  → INTEGRATION-READY → INTEGRATION VERIFIED
  → SYSTEM-VERIFIED → RELEASE
```

If verification fails: **STOP**.  
Do not normalize `--force` / `--skip-verification` / `--allow-unverified` as the production path.

---

## Four continuous questions

1. What already exists?  
2. What was actually fixed or added?  
3. What evidence proves it?  
4. What is still sealed and therefore not trusted?  

**Adopt what works. Fix what is broken. Build only what is missing. Seal what is unproven. Connect only what has passed its verification path.**
