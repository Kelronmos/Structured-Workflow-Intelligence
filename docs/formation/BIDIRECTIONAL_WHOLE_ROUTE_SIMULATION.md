# Bidirectional Whole-Route Simulation (proposed control)

**Package status:** `PROPOSED` · `NOT_IMPLEMENTED`  
**Proof status:** `NONE`  
**Seal / authorization / execution:** not claimed  
**Placement:** Main governance documentation only — **not** V1/V2 runtime  

## Purpose

Make **every forward transition** on FM-023–FM-040 a test point that must freeze/hash state, **trace backward**, **simulate forward**, **compare** planes (SCAR/risk/safety/ethics/normative/institutional/jurisdictional), and record findings **without** promoting UNKNOWN to SAFE / LEGAL / AUTHORIZED.

```text
PROPOSED CONTROL ≠ RUNTIME PIPE
SIMULATION SUCCESS ≠ EXECUTION AUTHORIZATION
DOCUMENTATION ≠ PROOF
```

## Relation to FM-023–FM-040

Construction order unchanged; **each arrow is a simulation boundary**. Inventory remains **NOT_IMPLEMENTED**.

## Per-transition algorithm (specification)

Steps 1–31: freeze → hash → trace back (origin, evidence, rules, authority, SCARs) → simulate transition and consequence variants (boundary, malformed, unauthorised, evidence-loss, authority-expiry, rule-conflict) → compare planes → map sources/jurisdictions → detect conflicts/UNKNOWNs → control decision → record → hash → continue only if control permits.

## Comparison planes

Technical · SCAR/Risk · Human/ethical · Normative/legal (cited sources) · Institutional · Cross-jurisdictional  

Unresolved conflicts → human/legal review. No auto “which law wins.”

## Finding shape

Prefer `legal_status: UNKNOWN`, `execution_authorized: false`, uncertainties listed. Never machine “this is legal/ethical” as settled truth.

```text
NORMATIVE LEVEL ≠ REQUIREMENT STRENGTH ≠ APPLICABILITY
≠ RISK ≠ AUTHORITY ≠ EXECUTION AUTHORIZATION
A1≠A2≠A3≠A4≠A5
```

## Heuristics

Common-sense / ethics: `OBSERVATION` | `WARNING` | `REVIEW_REQUIRED` | `UNKNOWN` only — not LEGAL/ILLEGAL; cannot override law or evidence.

## SCAR bridge

CONTINUE · MORE EVIDENCE · SCAR · SCAR+ESCALATION · SCAR+HUMAN REVIEW · HALT  

SCAR ≠ guilt ≠ illegality ≠ auto reject ≠ auto approve.

## Invariants

| ID | Statement |
|----|-----------|
| I-SIM-001 | No forward transition verified without evaluating provenance, state, consequences, rules, SCAR, authority, risk/impact (when pipe exists). |
| I-SIM-002 | UNKNOWN ≠ SAFE ≠ LEGAL ≠ ETHICAL ≠ AUTHORIZED ≠ APPROVED |
| I-SIM-003 | SIMULATION SUCCESS ≠ EXECUTION AUTHORIZATION |
| I-SIM-004 | Downstream consequence may reclassify earlier decision; history not erased. |
| I-SIM-005 | Later decision must not erase original evidence or rewrite history. |
| I-SIM-006 | Law, policy, ethics, common-sense, risk, SCAR, institutional authority remain separately identifiable. |

## Non-claims

Not implemented · not legal/ethical determination · not execution auth · not FM-023–040 runtime · not V1/V2 modification.

Machine index: `bidirectional_simulation_control.json`  
Schema: `schemas/formation/swi-simulation-finding.schema.json`
