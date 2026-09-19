# SWI seal evidence

This directory holds **seal records** for modules whose registry state is `SEALED`.

## Rules

- A registry flag is **never** evidence.
- `state: SEALED` requires a valid `seal_record.path` pointing here.
- Each record must satisfy `schemas/swi-seal-record.schema.json`.
- Required checks (all must be `true`):
  - contract
  - unit
  - negative
  - deterministic
  - security
  - reproducible
- Records must cite an immutable commit SHA and a run id (local or CI).
- Limitations must be explicit.

## Layout (create only when evidence exists)

```text
evidence/
├── M02/seal-record.json
├── M03/seal-record.json
├── ...
└── M11/seal-record.json
```

Empty directories or README files are **not** seals.

Do not create a `PASS` record until the six gates have actually passed against a known commit.

## Verify

```bash
node scripts/swi-seal.mjs
npm run swi:seal
```

Expected on unproven SEALED modules: **FAIL** (correct).
