# Allowed State Machine (SWI-GOV-REMEDIATION-001 §24)

```
DESIGN
  ↓
CONTRACT_FROZEN
  ↓
IMPLEMENTED
  ↓
TESTED
  ↓
CI_VERIFIED
  ↓
AUDITED
  ↓
SEALED
```

## Forbidden transitions

- DESIGN → SEALED
- IMPLEMENTED → SEALED
- README → SEALED
- REGISTRY declaration → SEALED

## Failure path

```
ANY STATE
  ↓
VERIFICATION FAILURE
  ↓
HALTED
```

A failed component must not automatically return to SEALED.

## Historical claims

If historical evidence cannot be recovered:

```
status: HISTORICAL_CLAIM_UNVERIFIED
```

rather than `state: SEALED`.
