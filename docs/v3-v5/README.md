# SWI v3–v5 documentation set

| Document | Role |
|----------|------|
| [SWI_V3_V5_FIX_ADOPTION_VERIFICATION_MANUAL.md](./SWI_V3_V5_FIX_ADOPTION_VERIFICATION_MANUAL.md) | Fix / adopt / seal / integrate doctrine |
| [../../SWI_V3_V4_V5_BUILD_MANUAL.md](../../SWI_V3_V4_V5_BUILD_MANUAL.md) | Controlled completion build manual |
| [../SWI_V3_V4_V5_SEALED_BUILD_MANUAL.md](../SWI_V3_V4_V5_SEALED_BUILD_MANUAL.md) | Commands for registry gates |
| [../../config/swi-module-registry.json](../../config/swi-module-registry.json) | Machine-readable module states |

```bash
node scripts/swi-verify-module.mjs
node --test tests/swi-module-registry.test.mjs
```
