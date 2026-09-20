# Formal route invariant & verification gate (proposed)

**Package status:** `PROPOSED` · `NOT_IMPLEMENTED`  
**Proof status:** `NONE`  
**Extends:** Bidirectional Whole-Route Simulation  
**Does not:** authorize execution, determine law/ethics, or implement FM-023–040

## Purpose

Every future module/step on the band must pass through the same freeze → trace-back → simulate → compare → control → evidence+hash mechanism.

```text
ROUTE_VERIFIED ≠ EXECUTION_AUTHORIZED
ROUTE_VERIFIED ≠ LEGAL DETERMINATION
ROUTE_VERIFIED ≠ ETHICAL DETERMINATION
ROUTE_VERIFIED ≠ INSTITUTIONAL AUTHORITY
```

## Mandatory per-step pipe

```text
FORWARD STEP → FREEZE STATE
  → TRACE BACK / TRACE FORWARD / SCAR·RISK·SAFETY
  → ETHICS / LAW·POLICY / AUTHORITY / JURISDICTION
  → BOUNDARY FAILURE TESTS / RECORD UNKNOWN·CONFLICT
  → CONTROL: CONTINUE | PAUSE | HALT
  → EVIDENCE + HASH → REPLAY → INDEPENDENT VERIFICATION
```

## Terminal-state justification (I-SIM-007)

A terminal **label alone is not evidence**.

| Terminal | Required justification |
|----------|------------------------|
| `FM-040` | Valid route completion; no undeclared skip |
| `PAUSED` | `pause_reason` non-null + evidence |
| `HALTED` | `halt_reason` non-null + evidence |
| `QUARANTINED` | `quarantine_reason` non-null + evidence |

**Rejected:** `FM-023 → FM-040` without route rule; `FM-023 → HALTED` without `halt_reason`.

### I-SIM-007

A TERMINAL STATE MUST BE JUSTIFIED BY THE EVIDENCE, CONTROL CONDITION, AND TRANSITION THAT PRODUCED IT. A TERMINAL LABEL ALONE IS NOT EVIDENCE.

### I-SIM-008

NO TRANSITION MAY SKIP A REQUIRED FORMATION PATH WITHOUT AN EXPLICIT, EVIDENCE-BOUND ROUTE RULE.

## Route-delta record

Every transition records hashes, changed fields, evidence add/remove, risks, SCARs, authority/jurisdiction/rule changes. `execution_authorization_change` stays false in this package.

## ROUTE_VERIFIED gate (future)

Conjunction includes: SOURCE_BOUND, EXACT_SHA_BOUND, PREDECESSOR/SUCCESSOR_VALID, NO_UNDECLARED_SKIP, BACKWARD/FORWARD_TRACE_COMPLETE, CONSEQUENCE_SIMULATED, SCAR/RISK/HUMAN_IMPACT_CHECKED, NORMATIVE_SOURCES_BOUND, APPLICABILITY/AUTHORITY/JURISDICTION/CONFLICTS recorded, UNKNOWNS_PRESERVED, EVIDENCE_INTEGRITY_VALID, TAMPER_TESTED, REPLAYABLE, **TERMINAL_JUSTIFIED**.

Even if `ROUTE_VERIFIED = true`, `EXECUTION_AUTHORIZED` remains independent and false unless a separate authority gate sets it.

## Schemas

- `schemas/formation/swi-route-delta.schema.json`
- `schemas/formation/swi-route-transition.schema.json`
- `schemas/formation/swi-route-verified.schema.json`

## Non-claims

Not implemented · not compliance oracle · not V1/V2 runtime · not FM-023–040 execution.
