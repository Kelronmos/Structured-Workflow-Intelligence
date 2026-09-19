# FAILURE POLICY

## Rule

**FAILURE = NO EXECUTION**

A failed gate must produce:

1. machine-readable JSON
2. deterministic evidence record
3. SHA-256 hash
4. human-readable report
5. explicit failure reason
6. observed state
7. required state
8. module
9. dependency (if applicable)
10. commit
11. contract hash

## Example HALT Event

```json
{
  "event": "ADMISSION_HALTED",
  "module": "V2-M13",
  "reason": "DEPENDENCY_NOT_SEALED",
  "required": "SEALED",
  "observed": "IMPLEMENTED",
  "dependency": "V2-M12",
  "action": "HALT"
}
```

The system must not continue after this event.

## Storage

- `evidence/json/<event-id>.json`
- `evidence/hashes/<event-id>.sha256`
- `evidence/reports/<event-id>.txt`
