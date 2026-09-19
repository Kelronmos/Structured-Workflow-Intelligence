# Execution mode declaration policy

**Status:** Research policy (from V4→V5 patch intent)  
**Does not** authorize production deployment.

## Requirement

Modules and runtime components SHOULD declare an explicit execution mode:

| Mode | Meaning |
|------|---------|
| `REAL` | Implemented path with executable tests and evidence |
| `HYBRID` | Mix of real controls and simulated subsystems |
| `SIMULATED` | Model, stub, or demonstration only |

## Rules

1. No component may claim security properties without a corresponding verification function and evidence.
2. Missing implementation → mark `SIMULATED` or remove the claim.
3. `SEALED` registry state still requires `evidence/` seal records (see `scripts/swi-seal.mjs`).
4. Runtime events that claim integrity SHOULD eventually emit hash / signature / timestamp / prevHash — only when the implementation exists and is tested.

## Alignment

- `SWI_SYSTEM_STATE.json`: RESEARCH_PROTOTYPE / DO_NOT_DEPLOY
- `GOVERNANCE_RULES.md`: no production-ready security representation
- Seal gate: evidence before status
