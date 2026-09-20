# Seal gate status (Main)

**Artifacts:** `schemas/swi-seal-record.schema.json` · `scripts/swi-seal.mjs`  
**Invariant:** registry `SEALED` ⇒ `seal_record.path` under `evidence/` with schema-valid PASS checks.

## First-run expectation

M11 is `state: SEALED` without `seal_record` ⇒

```bash
node scripts/swi-seal.mjs
# SWI SEAL GATE: FAILED
# M11: SEALED requires seal_record.path
```

That failure is **correct**. Do not invent PASS files to clear it.

## Non-claims

Adding the gate does not newly seal modules, set `production_ready`, or enable integration.

## Next

Revalidate → real `evidence/MXX/seal-record.json` → registry path → gate PASS only then.
