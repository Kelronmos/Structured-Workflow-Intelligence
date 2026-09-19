# Workflow Activation Policy

**Status:** MANDATORY  
**Authority:** Governance Authority  
**Default:** DENY activation unless verified

## Principle

> Discovery does not equal activation.  
> YAML exists does not equal trusted.  
> Location under `.github/workflows/` is the only path to automatic GitHub Actions execution.

## Allowed activation states

| State | Meaning |
|-------|---------|
| DISCOVERED | Found on disk |
| REVIEW_REQUIRED | Candidate needs authority/permissions/secrets/dependency review |
| VERIFIED | Reviews complete; still not active |
| ACTIVATION_AUTHORIZED | Explicit governance decision recorded |
| ACTIVE | Under `.github/workflows/` and executed by GitHub |
| BLOCKED | Must not be activated |
| RETIRED | Intentionally disabled |

## Forbidden transition

```
YAML exists → trusted → active
```

## Required gate before MOVE/ACTIVATE

```
DISCOVER
  ↓
CLASSIFY
  ↓
CONTRACT
  ↓
DEPENDENCY / AUTHORITY REVIEW
  ↓
SECURITY REVIEW
  ↓
TEST
  ↓
MOVE/ACTIVATE
  ↓
CI VERIFY
  ↓
EVIDENCE + HASH
```

## Checks before activation authorization

- Under `.github/workflows/` only after authorization
- YAML parses
- Trigger identified
- Permissions identified
- Secrets/environment access identified
- Write/deploy capabilities identified
- Dependencies identified
- Governance authority identified
- Referenced tests exist
- Script/file references resolve
- No prohibited bypass of admission/HALT
- Route provenance coverage (where applicable)
- Determinism/isolation requirements (where applicable)
- Evidence output defined
- Failure behavior defined (HALT/FAIL)
- Explicit activation decision recorded

## Current authority

```
workflow_activation_authority: DENIED_UNLESS_VERIFIED
governance_backbone:
  state: NOT_SEALED
  execution_authority: DENIED
```

Legacy `.github/*.yml` files are preserved and inventoried. They are not moved into `workflows/` by this policy alone.
