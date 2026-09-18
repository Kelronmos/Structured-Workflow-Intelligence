# SWI v3–v5 Sealed Build Controls

Canonical process manual (root):

**[SWI_V3_V4_V5_BUILD_MANUAL.md](../SWI_V3_V4_V5_BUILD_MANUAL.md)**

## Repository controls (this commit family)

| Artifact | Role |
|----------|------|
| `config/swi-module-registry.json` | Module states M01–M15, seal levels, verification flags |
| `scripts/swi-verify-module.mjs` | Registry consistency + dependency gating |
| `tests/swi-module-registry.test.mjs` | Prevent accidental `production_ready` / integration |
| `MODULE_REGISTRY.json` | High-level cross-repo registry (companion) |

## Commands

```bash
node scripts/swi-verify-module.mjs
node scripts/swi-verify-module.mjs M11
node --test tests/swi-module-registry.test.mjs
```

## Governing path

```text
DISCOVER → ADOPT EXISTING → IDENTIFY GAPS → BUILD ONLY MISSING
  → TEST → VERIFY → SEAL → INTEGRATION-READY → CONNECT
  → SYSTEM VERIFY → RELEASE
```

**M11 / M12:** remain **SEALED**, `integration_enabled=false`, until evidence justifies promotion.

Do not treat registry rows as production certification.
