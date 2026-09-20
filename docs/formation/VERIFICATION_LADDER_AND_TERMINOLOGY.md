# Verification ladder & terminology (freeze)

**Purpose:** Prevent over-claiming. Schema/negative-control ≠ formal verification of an implemented system. TLA+ MODEL_PASS ≠ runtime implementation.

## Precise claims for current Main artifacts

| Claim | Status |
|-------|--------|
| Schema-level machine-checkable constraints | **Yes** (formation + simulation schemas) |
| Negative-control verification | **PASS** (recorded) |
| TLA+ **abstract** route model + TLC | **MODEL_PASS** (`formal/tla/`, commit lineage including `d1483964`) |
| FM-023–040 **runtime** implementation | **NOT_IMPLEMENTED** |
| Legal / ethical / production authorization | **No** |

Prefer:

> Schema-level constraint verification / negative-control verification  
> and, separately, **finite-model TLC verification** of an abstract TLA+ route machine.

Do not collapse either into “the SWI system is formally verified.”

## Status ledger (reconciled)

```text
DOCUMENTED
    ↓
SCHEMA-CONSTRAINED
    ↓
NEGATIVE-CONTROL VERIFIED          ← formation + simulation packages
    ↓
FORMAL MODEL (abstract TLA+)       ← STARTED: formal/tla/
    ↓
MODEL CHECKED (finite abstract)    ← MODEL_PASS recorded; mutations COUNTEREXAMPLE
    ↓
[IMPLEMENTATION]                   ← NOT STARTED (runtime)
    ↓
IMPLEMENTATION VERIFICATION
    ↓
INDEPENDENT VERIFICATION
```

## Package flags (unchanged intent)

```text
PROPOSED / NOT_IMPLEMENTED     (runtime FM band)
proof_status: NONE             (no system-level proof claim)
execution: NOT_EXECUTABLE
negative_control: PASS
formal_model_construction: STARTED (abstract only)
tla_model_status: MODEL_PASS   (within MaxStep=26 model + assumptions)
```

## Evidence layers stay separate

```text
Schema constraint
    ≠ negative-control verification
    ≠ TLA+ model verification
    ≠ implementation verification
    ≠ legal determination
    ≠ ethical determination
    ≠ institutional authority
    ≠ execution authorization
```

## If TLC = PASS (current abstract model)

Bounded statement only:

> The specified invariants hold for the explored finite model under its recorded constants, abstractions, and assumptions.

Does **not** promote Main package, V1, or V2 to implemented, sealed, legal, or execution-authorized.

## Pointers

| Artifact | Role |
|----------|------|
| `docs/formation/*` | Design + schemas + negative controls |
| `formal/tla/` | Abstract TLA+ model + MutA–F + TLC result |
| `formal/tla/TLA_MODEL_CHECK_RESULT.json` | MODEL_PASS evidence object |

V1 FM-001–013 and V2 M11–M22 remain independent.
