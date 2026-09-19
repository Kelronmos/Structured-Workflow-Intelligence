# Seal Records Directory

This directory holds the independent seal records required for any module whose
`state` is declared `SEALED` in `MODULE_REGISTRY.yaml`.

## Rule (enforced by CI)

```
SEALED
  ↓
seal record exists?   (governance/seal_records/<MODULE_ID>.yaml|.json|.md)
  ↓ NO
CI FAILURE / HALT
```

There is no warning-only path.

## Required content (see SEAL_POLICY.md)

- contract.path + contract.sha256
- implementation.commit + implementation.sha256
- tests (total / passed / failed)
- ci (workflow / run_id / conclusion)
- dependencies (required + verified)
- limitations
- evidence.report + evidence.sha256
- sealed_at

Until a real seal record is placed here for a module, that module must not remain
in the `SEALED` state in the registry.
