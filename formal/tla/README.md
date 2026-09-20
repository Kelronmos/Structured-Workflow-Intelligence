# TLA+ abstract route model (formal model only)

**Status:** `FORMAL_MODEL` · runtime `NOT_IMPLEMENTED` · execution `NOT_EXECUTABLE`

## Source design commits

`77f4761c` · `4348cfa4` · `57f0d968` · `6f943a1f`

## Layout

| Path | Role |
|------|------|
| `route_model/SWIRouteModel.tla` | Positive abstract machine |
| `mutations/MutA..F` | Deliberate violations (expect counterexamples) |
| `TLA_MODEL_CHECK_RESULT.*` | Recorded TLC evidence |

```bash
java -cp tla2tools.jar tlc2.TLC -config formal/tla/route_model/SWIRouteModel.cfg formal/tla/route_model/SWIRouteModel.tla
```

```text
MODEL_PASS ≠ IMPLEMENTATION ≠ LEGAL ≠ EXECUTION_AUTHORIZED
```
