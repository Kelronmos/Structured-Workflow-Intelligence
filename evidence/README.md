# Seal evidence tree

**Rule:** Do not place fabricated `PASS` seal records here solely to green the gate.

| Path | Meaning |
|------|---------|
| `evidence/MXX/seal-record.json` | Required when registry `state` is `SEALED` |
| Empty dirs | Allowed — no seal evidence yet |

`scripts/swi-seal.mjs` fails if any module is `SEALED` without a valid record under this tree.

Historical V2 `docs/M11_SEAL_RECORD.md` is not auto-accepted; bind via schema-valid `seal-record.json` only after revalidation.
