# SEAL POLICY

## Required Seal Record

```yaml
module:
version:
module_id:

state: SEALED

contract:
  path:
  sha256:

implementation:
  commit:
  sha256:

tests:
  total:
  passed:
  failed:

ci:
  workflow:
  run_id:
  conclusion:

dependencies:
  required:
  verified:

limitations:

evidence:
  report:
  sha256:

sealed_at:
```

## Validity Conditions

A seal is valid only when **all** of the following are true:

- contract hash matches
- implementation commit matches
- tests pass
- CI passes
- dependencies pass
- seal record is internally consistent

Otherwise: **HALT**

## Core Distinction

SEALED means:
> the specified contract was implemented at the specified commit and passed the specified verification boundary.

SEALED does **not** mean:
- truth
- AI safety
- production readiness
- legal compliance
- global correctness
- security certification
- business approval
- human approval

Those claims require separate evidence.
