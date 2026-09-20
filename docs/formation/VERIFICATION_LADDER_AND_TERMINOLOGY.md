# Verification ladder & terminology (freeze)

**Purpose:** Prevent over-claiming. The Main formation package is **not** formal verification of an implemented system.

**Package status (unchanged):** `PROPOSED` / `NOT_IMPLEMENTED` · `proof_status: NONE` · `execution: NOT_EXECUTABLE`

## Precise claim for current Main artifacts

| Claim | Legitimate? |
|-------|-------------|
| Schema-level machine-checkable constraint verification | **Yes** (where schemas + verifiers exist) |
| Negative-control verification (prohibited states rejected) | **Yes** (`NEGATIVE_CONTROL_RESULT = PASS` where recorded) |
| Formal verification of an implemented simulator/route runtime | **No** |
| Model checked / SMT-proven system | **No** (future) |
| Legal / ethical / production authorization | **No** |

Prefer the phrase:

> Schema-level machine-checkable constraint verification / negative-control verification.

Avoid calling the current result simply “formal verification.”

## Status ledger

```text
DOCUMENTED
    ↓
SCHEMA-CONSTRAINED
    ↓
NEGATIVE-CONTROL VERIFIED          ← Main formation package is here
    ↓
[FORMAL MODEL CONSTRUCTION]        ← future construction repo only
    ↓
MODEL CHECKED
    ↓
[IMPLEMENTATION]
    ↓
CONTRACT VERIFIED
    ↓
SYMBOLIC / ADVERSARIAL VERIFIED
    ↓
RUNTIME MONITORED
    ↓
INDEPENDENTLY RECHECKED
```

## What each level may claim

| Level | Legitimate claim |
|-------|------------------|
| Schema validation | Data conforms to structural constraints |
| Negative controls | Selected prohibited states are rejected |
| Model checking | All reachable states **in the defined model** satisfy specified properties |
| SMT / symbolic | No counterexample **within the encoding** (e.g. UNSAT) |
| Contract verification | Specified functions satisfy pre/postconditions |
| Theorem proving | Propositions proven under stated axioms |
| Independent verification | Separate party reproduces/checks the result |

## Future formal properties (construction repo only — not claimed here)

P1 `ROUTE_VERIFIED(x) → ¬EXECUTION_AUTHORIZED(x)`  
P2 terminal ∈ {PAUSED, HALTED, QUARANTINED} → reason ≠ ∅ ∧ evidence_bound  
P3 skip(a,b) → explicit route rule ∧ evidence-bound  
P4 UNKNOWN → ¬SAFE ∧ ¬LEGAL ∧ ¬APPROVED  
P5 authority non-expansion without explicit capability  
P6 unresolved mandatory condition → ¬EXECUTION_AUTHORIZED  
P7 evidence removed → route-delta.removed_evidence ≠ ∅  
P8 SCAR → ¬ automatic ILLEGAL / GUILTY / APPROVED  

Solver target form: `EXISTS prohibited_condition` → desire **UNSAT** under stated assumptions. **SAT** is useful (counterexample), not a failure to hide.

## Even future MODEL_CHECK = PASS still means

```text
property holds within model + assumptions + encoding
  ≠ real-world software correct
  ≠ legal / ethical / secure / safe / authorized / production-ready
```

## Freeze pointer

| Artifact | Role |
|----------|------|
| FM-023–040 inventory + five-axis schemas | DOCUMENTED / SCHEMA-CONSTRAINED |
| Simulation + route invariant package | DOCUMENTED / SCHEMA-CONSTRAINED |
| `verify_formation_package.py` | NEGATIVE-CONTROL (inventory/axes) |
| `verify_simulation_control_negative.py` | NEGATIVE-CONTROL (simulation/route schemas) |

V1 FM-001–013 and V2 M11–M22 are **not** altered by this package.

```text
PROPOSED / NOT_IMPLEMENTED
proof_status: NONE
execution: NOT_EXECUTABLE
negative_control: PASS (where reports exist)
formal model construction: NOT STARTED on Main
```
